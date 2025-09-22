from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.managers.zip_downloads import DownloadZipItems

from box_sdk_gen.managers.zip_downloads import DownloadZipItemsTypeField

from box_sdk_gen.schemas.zip_download import ZipDownload

from box_sdk_gen.managers.zip_downloads import CreateZipDownloadItems

from box_sdk_gen.schemas.zip_download_status import ZipDownloadStatus

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import upload_new_file

from test.box_sdk_gen.test.commons import create_new_folder

from box_sdk_gen.internal.utils import buffer_equals

from box_sdk_gen.internal.utils import read_byte_stream

from box_sdk_gen.internal.utils import generate_byte_buffer

from box_sdk_gen.internal.utils import date_time_to_string

client: BoxClient = get_default_client()


def testZipDownload():
    file_1: FileFull = upload_new_file()
    file_2: FileFull = upload_new_file()
    folder_1: FolderFull = create_new_folder()
    zip_stream: ByteStream = client.zip_downloads.download_zip(
        [
            DownloadZipItems(id=file_1.id, type=DownloadZipItemsTypeField.FILE),
            DownloadZipItems(id=file_2.id, type=DownloadZipItemsTypeField.FILE),
            DownloadZipItems(id=folder_1.id, type=DownloadZipItemsTypeField.FOLDER),
        ],
        download_file_name='zip',
    )
    assert (
        buffer_equals(read_byte_stream(zip_stream), generate_byte_buffer(10)) == False
    )
    client.files.delete_file_by_id(file_1.id)
    client.files.delete_file_by_id(file_2.id)
    client.folders.delete_folder_by_id(folder_1.id)


def testManualZipDownloadAndCheckStatus():
    file_1: FileFull = upload_new_file()
    file_2: FileFull = upload_new_file()
    folder_1: FolderFull = create_new_folder()
    zip_download: ZipDownload = client.zip_downloads.create_zip_download(
        [
            CreateZipDownloadItems(id=file_1.id, type=DownloadZipItemsTypeField.FILE),
            CreateZipDownloadItems(id=file_2.id, type=DownloadZipItemsTypeField.FILE),
            CreateZipDownloadItems(
                id=folder_1.id, type=DownloadZipItemsTypeField.FOLDER
            ),
        ],
        download_file_name='zip',
    )
    assert not zip_download.download_url == ''
    assert not zip_download.status_url == ''
    assert not date_time_to_string(zip_download.expires_at) == ''
    zip_stream: ByteStream = client.zip_downloads.get_zip_download_content(
        zip_download.download_url
    )
    assert (
        buffer_equals(read_byte_stream(zip_stream), generate_byte_buffer(10)) == False
    )
    zip_download_status: ZipDownloadStatus = (
        client.zip_downloads.get_zip_download_status(zip_download.status_url)
    )
    assert zip_download_status.total_file_count == 2
    assert zip_download_status.downloaded_file_count == 2
    assert zip_download_status.skipped_file_count == 0
    assert zip_download_status.skipped_folder_count == 0
    assert not to_string(zip_download_status.state) == 'failed'
    client.files.delete_file_by_id(file_1.id)
    client.files.delete_file_by_id(file_2.id)
    client.folders.delete_folder_by_id(folder_1.id)
