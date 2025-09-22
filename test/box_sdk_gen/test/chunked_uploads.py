from typing import List

from box_sdk_gen.internal.utils import to_string

from typing import Optional

from box_sdk_gen.internal.utils import Buffer

from box_sdk_gen.internal.utils import HashName

from box_sdk_gen.internal.utils import Iterator

from box_sdk_gen.internal.utils import generate_byte_stream_from_buffer

from box_sdk_gen.internal.utils import hex_to_base_64

from box_sdk_gen.internal.utils import iterate_chunks

from box_sdk_gen.internal.utils import read_byte_stream

from box_sdk_gen.internal.utils import reduce_iterator

from box_sdk_gen.internal.utils import Hash

from box_sdk_gen.internal.utils import buffer_length

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import generate_byte_stream

from box_sdk_gen.internal.utils import ByteStream

from test.box_sdk_gen.test.commons import get_default_client

from box_sdk_gen.schemas.file import File

from box_sdk_gen.schemas.upload_session import UploadSession

from box_sdk_gen.schemas.upload_part import UploadPart

from box_sdk_gen.schemas.upload_parts import UploadParts

from box_sdk_gen.schemas.uploaded_part import UploadedPart

from box_sdk_gen.schemas.files import Files

from box_sdk_gen.client import BoxClient

client: BoxClient = get_default_client()


class _TestPartAccumulator:
    def __init__(
        self,
        last_index: int,
        parts: List[UploadPart],
        file_size: int,
        file_hash: Hash,
        *,
        upload_part_url: str = '',
        upload_session_id: str = ''
    ):
        self.last_index = last_index
        self.parts = parts
        self.file_size = file_size
        self.file_hash = file_hash
        self.upload_part_url = upload_part_url
        self.upload_session_id = upload_session_id


def _reducer_by_id(
    acc: _TestPartAccumulator, chunk: ByteStream
) -> _TestPartAccumulator:
    last_index: int = acc.last_index
    parts: List[UploadPart] = acc.parts
    chunk_buffer: Buffer = read_byte_stream(chunk)
    hash: Hash = Hash(algorithm=HashName.SHA1)
    hash.update_hash(chunk_buffer)
    sha_1: str = hash.digest_hash('base64')
    digest: str = ''.join(['sha=', sha_1])
    chunk_size: int = buffer_length(chunk_buffer)
    bytes_start: int = last_index + 1
    bytes_end: int = last_index + chunk_size
    content_range: str = ''.join(
        [
            'bytes ',
            to_string(bytes_start),
            '-',
            to_string(bytes_end),
            '/',
            to_string(acc.file_size),
        ]
    )
    uploaded_part: UploadedPart = client.chunked_uploads.upload_file_part(
        acc.upload_session_id,
        generate_byte_stream_from_buffer(chunk_buffer),
        digest,
        content_range,
    )
    part: UploadPart = uploaded_part.part
    part_sha_1: str = hex_to_base_64(part.sha_1)
    assert part_sha_1 == sha_1
    assert part.size == chunk_size
    assert part.offset == bytes_start
    acc.file_hash.update_hash(chunk_buffer)
    return _TestPartAccumulator(
        last_index=bytes_end,
        parts=parts + [part],
        file_size=acc.file_size,
        upload_session_id=acc.upload_session_id,
        file_hash=acc.file_hash,
    )


def testChunkedManualProcessById():
    file_size: int = (20 * 1024) * 1024
    file_byte_stream: ByteStream = generate_byte_stream(file_size)
    file_name: str = get_uuid()
    parent_folder_id: str = '0'
    upload_session: UploadSession = client.chunked_uploads.create_file_upload_session(
        parent_folder_id, file_size, file_name
    )
    upload_session_id: str = upload_session.id
    part_size: int = upload_session.part_size
    total_parts: int = upload_session.total_parts
    assert part_size * total_parts >= file_size
    assert upload_session.num_parts_processed == 0
    file_hash: Hash = Hash(algorithm=HashName.SHA1)
    chunks_iterator: Iterator = iterate_chunks(file_byte_stream, part_size, file_size)
    results: _TestPartAccumulator = reduce_iterator(
        chunks_iterator,
        _reducer_by_id,
        _TestPartAccumulator(
            last_index=-1,
            parts=[],
            file_size=file_size,
            upload_session_id=upload_session_id,
            file_hash=file_hash,
        ),
    )
    parts: List[UploadPart] = results.parts
    processed_session_parts: UploadParts = (
        client.chunked_uploads.get_file_upload_session_parts(upload_session_id)
    )
    assert processed_session_parts.total_count == total_parts
    processed_session: UploadSession = (
        client.chunked_uploads.get_file_upload_session_by_id(upload_session_id)
    )
    assert processed_session.id == upload_session_id
    sha_1: str = file_hash.digest_hash('base64')
    digest: str = ''.join(['sha=', sha_1])
    committed_session: Optional[Files] = (
        client.chunked_uploads.create_file_upload_session_commit(
            upload_session_id, parts, digest
        )
    )
    assert committed_session.entries[0].name == file_name
    client.chunked_uploads.delete_file_upload_session_by_id(upload_session_id)


def _reducer_by_url(
    acc: _TestPartAccumulator, chunk: ByteStream
) -> _TestPartAccumulator:
    last_index: int = acc.last_index
    parts: List[UploadPart] = acc.parts
    chunk_buffer: Buffer = read_byte_stream(chunk)
    hash: Hash = Hash(algorithm=HashName.SHA1)
    hash.update_hash(chunk_buffer)
    sha_1: str = hash.digest_hash('base64')
    digest: str = ''.join(['sha=', sha_1])
    chunk_size: int = buffer_length(chunk_buffer)
    bytes_start: int = last_index + 1
    bytes_end: int = last_index + chunk_size
    content_range: str = ''.join(
        [
            'bytes ',
            to_string(bytes_start),
            '-',
            to_string(bytes_end),
            '/',
            to_string(acc.file_size),
        ]
    )
    uploaded_part: UploadedPart = client.chunked_uploads.upload_file_part_by_url(
        acc.upload_part_url,
        generate_byte_stream_from_buffer(chunk_buffer),
        digest,
        content_range,
    )
    part: UploadPart = uploaded_part.part
    part_sha_1: str = hex_to_base_64(part.sha_1)
    assert part_sha_1 == sha_1
    assert part.size == chunk_size
    assert part.offset == bytes_start
    acc.file_hash.update_hash(chunk_buffer)
    return _TestPartAccumulator(
        last_index=bytes_end,
        parts=parts + [part],
        file_size=acc.file_size,
        upload_part_url=acc.upload_part_url,
        file_hash=acc.file_hash,
    )


def testChunkedManualProcessByUrl():
    file_size: int = (20 * 1024) * 1024
    file_byte_stream: ByteStream = generate_byte_stream(file_size)
    file_name: str = get_uuid()
    parent_folder_id: str = '0'
    upload_session: UploadSession = client.chunked_uploads.create_file_upload_session(
        parent_folder_id, file_size, file_name
    )
    upload_part_url: str = upload_session.session_endpoints.upload_part
    commit_url: str = upload_session.session_endpoints.commit
    list_parts_url: str = upload_session.session_endpoints.list_parts
    status_url: str = upload_session.session_endpoints.status
    abort_url: str = upload_session.session_endpoints.abort
    upload_session_id: str = upload_session.id
    part_size: int = upload_session.part_size
    total_parts: int = upload_session.total_parts
    assert part_size * total_parts >= file_size
    assert upload_session.num_parts_processed == 0
    file_hash: Hash = Hash(algorithm=HashName.SHA1)
    chunks_iterator: Iterator = iterate_chunks(file_byte_stream, part_size, file_size)
    results: _TestPartAccumulator = reduce_iterator(
        chunks_iterator,
        _reducer_by_url,
        _TestPartAccumulator(
            last_index=-1,
            parts=[],
            file_size=file_size,
            upload_part_url=upload_part_url,
            file_hash=file_hash,
        ),
    )
    parts: List[UploadPart] = results.parts
    processed_session_parts: UploadParts = (
        client.chunked_uploads.get_file_upload_session_parts_by_url(list_parts_url)
    )
    assert processed_session_parts.total_count == total_parts
    processed_session: UploadSession = (
        client.chunked_uploads.get_file_upload_session_by_url(status_url)
    )
    assert processed_session.id == upload_session_id
    sha_1: str = file_hash.digest_hash('base64')
    digest: str = ''.join(['sha=', sha_1])
    committed_session: Optional[Files] = (
        client.chunked_uploads.create_file_upload_session_commit_by_url(
            commit_url, parts, digest
        )
    )
    assert committed_session.entries[0].name == file_name
    client.chunked_uploads.delete_file_upload_session_by_url(abort_url)


def testChunkedUploadConvenienceMethod():
    file_size: int = (20 * 1024) * 1024
    file_byte_stream: ByteStream = generate_byte_stream(file_size)
    file_name: str = get_uuid()
    parent_folder_id: str = '0'
    uploaded_file: File = client.chunked_uploads.upload_big_file(
        file_byte_stream, file_name, file_size, parent_folder_id
    )
    assert uploaded_file.name == file_name
    assert uploaded_file.size == file_size
    assert uploaded_file.parent.id == parent_folder_id
    client.files.delete_file_by_id(uploaded_file.id)
