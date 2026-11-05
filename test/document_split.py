from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.schemas.v2026_r0.document_split_create_response_v2026_r0 import (
    DocumentSplitCreateResponseV2026R0,
)

from box_sdk_gen.managers.document_split import CreateDocumentSplitV2026R0InputSource

from box_sdk_gen.schemas.v2026_r0.document_split_create_request_manual_v2026_r0 import (
    DocumentSplitCreateRequestManualV2026R0SplitTypeField,
)

from box_sdk_gen.schemas.v2026_r0.document_split_page_range_v2026_r0 import (
    DocumentSplitPageRangeV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.document_split_v2026_r0 import DocumentSplitV2026R0

from box_sdk_gen.schemas.v2026_r0.document_splits_v2026_r0 import DocumentSplitsV2026R0

from box_sdk_gen.internal.utils import get_uuid

from test.commons import get_default_client

from test.commons import upload_new_file

from test.commons import create_new_folder

from box_sdk_gen.schemas.v2026_r0.document_split_create_request_manual_v2026_r0 import (
    DocumentSplitCreateRequestManualV2026R0,
)

client: BoxClient = get_default_client()


def testCreateDocumentSplitV2026R0():
    file: FileFull = upload_new_file()
    folder: FolderFull = create_new_folder()
    external_id: str = get_uuid()
    created_document_split: DocumentSplitCreateResponseV2026R0 = (
        client.document_split.create_document_split_v2026_r0(
            file.id,
            folder.id,
            CreateDocumentSplitV2026R0InputSource.API,
            DocumentSplitCreateRequestManualV2026R0(
                split_type=DocumentSplitCreateRequestManualV2026R0SplitTypeField.MANUAL,
                split_definition=[DocumentSplitPageRangeV2026R0(start=1, end=1)],
            ),
            external_id=external_id,
        )
    )
    assert not created_document_split.id == ''
    assert to_string(created_document_split.type) == 'document_split'
    document_split: DocumentSplitV2026R0 = (
        client.document_split.get_document_split_by_id_v2026_r0(
            created_document_split.id
        )
    )
    assert document_split.id == created_document_split.id
    assert to_string(document_split.type) == 'document_split'
    assert document_split.source_file.id == file.id
    assert document_split.destination_folder.id == folder.id
    assert to_string(document_split.input_source) == 'api'
    assert not to_string(document_split.status) == ''
    assert document_split.external_id == external_id
    client.folders.delete_folder_by_id(folder.id, recursive=True)
    client.files.delete_file_by_id(file.id)


def testGetDocumentSplitsV2026R0():
    document_splits: DocumentSplitsV2026R0 = (
        client.document_split.get_document_splits_v2026_r0(limit=10)
    )
    assert len(document_splits.entries) >= 0
