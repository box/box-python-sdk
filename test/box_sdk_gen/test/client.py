from box_sdk_gen.internal.utils import to_string

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.serialization.json import SerializedData

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.managers.folders import CreateFolderParent

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.internal.utils import Buffer

from box_sdk_gen.schemas.files import Files

from box_sdk_gen.managers.uploads import UploadFileAttributes

from box_sdk_gen.managers.uploads import UploadFileAttributesParentField

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.user_full import UserFull

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import generate_byte_stream

from box_sdk_gen.internal.utils import buffer_equals

from box_sdk_gen.internal.utils import generate_byte_buffer

from box_sdk_gen.internal.utils import generate_byte_stream_from_buffer

from box_sdk_gen.internal.utils import read_byte_stream

from test.box_sdk_gen.test.commons import get_default_client

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_options import MultipartItem

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.networking.base_urls import BaseUrls

from box_sdk_gen.serialization.json import json_to_serialized_data

from box_sdk_gen.serialization.json import get_sd_value_by_key

client: BoxClient = get_default_client()


def testMakeRequestJsonCRUD():
    new_folder_name: str = get_uuid()
    request_body_post: str = ''.join(
        ['{"name": "', new_folder_name, '", "parent": { "id": "0"}}']
    )
    create_folder_response: FetchResponse = client.make_request(
        FetchOptions(
            method='post',
            url='https://api.box.com/2.0/folders',
            data=json_to_serialized_data(request_body_post),
        )
    )
    assert create_folder_response.status == 201
    created_folder: SerializedData = create_folder_response.data
    assert get_sd_value_by_key(created_folder, 'name') == new_folder_name
    updated_name: str = get_uuid()
    request_body_put: str = ''.join(['{"name": "', updated_name, '"}'])
    update_folder_response: FetchResponse = client.make_request(
        FetchOptions(
            method='put',
            url=''.join(
                [
                    'https://api.box.com/2.0/folders/',
                    get_sd_value_by_key(created_folder, 'id'),
                ]
            ),
            data=json_to_serialized_data(request_body_put),
        )
    )
    assert update_folder_response.status == 200
    updated_folder: SerializedData = update_folder_response.data
    assert get_sd_value_by_key(updated_folder, 'name') == updated_name
    assert get_sd_value_by_key(updated_folder, 'id') == get_sd_value_by_key(
        created_folder, 'id'
    )
    get_folder_response: FetchResponse = client.make_request(
        FetchOptions(
            url=''.join(
                [
                    'https://api.box.com/2.0/folders/',
                    get_sd_value_by_key(created_folder, 'id'),
                ]
            ),
            method='GET',
        )
    )
    assert get_folder_response.status == 200
    received_folder: SerializedData = get_folder_response.data
    assert get_sd_value_by_key(received_folder, 'name') == updated_name
    assert get_sd_value_by_key(received_folder, 'id') == get_sd_value_by_key(
        updated_folder, 'id'
    )
    delete_folder_response: FetchResponse = client.make_request(
        FetchOptions(
            url=''.join(
                [
                    'https://api.box.com/2.0/folders/',
                    get_sd_value_by_key(received_folder, 'id'),
                ]
            ),
            method='DELETE',
        )
    )
    assert delete_folder_response.status == 204


def testMakeRequestMultipart():
    new_folder_name: str = get_uuid()
    new_folder: FolderFull = client.folders.create_folder(
        new_folder_name, CreateFolderParent(id='0')
    )
    new_folder_id: str = new_folder.id
    new_file_name: str = ''.join([get_uuid(), '.pdf'])
    file_content_stream: ByteStream = generate_byte_stream(1024 * 1024)
    multipart_attributes: str = ''.join(
        ['{"name": "', new_file_name, '", "parent": { "id":', new_folder_id, '}}']
    )
    upload_file_response: FetchResponse = client.make_request(
        FetchOptions(
            method='POST',
            url='https://upload.box.com/api/2.0/files/content',
            content_type='multipart/form-data',
            multipart_data=[
                MultipartItem(
                    part_name='attributes',
                    data=json_to_serialized_data(multipart_attributes),
                ),
                MultipartItem(part_name='file', file_stream=file_content_stream),
            ],
        )
    )
    assert upload_file_response.status == 201
    client.folders.delete_folder_by_id(new_folder_id, recursive=True)


def testMakeRequestBinaryFormat():
    new_file_name: str = get_uuid()
    file_buffer: Buffer = generate_byte_buffer(1024 * 1024)
    file_content_stream: ByteStream = generate_byte_stream_from_buffer(file_buffer)
    uploaded_files: Files = client.uploads.upload_file(
        UploadFileAttributes(
            name=new_file_name, parent=UploadFileAttributesParentField(id='0')
        ),
        file_content_stream,
    )
    uploaded_file: FileFull = uploaded_files.entries[0]
    download_file_response: FetchResponse = client.make_request(
        FetchOptions(
            method='GET',
            url=''.join(
                ['https://api.box.com/2.0/files/', uploaded_file.id, '/content']
            ),
            response_format=ResponseFormat.BINARY,
        )
    )
    assert download_file_response.status == 200
    assert buffer_equals(read_byte_stream(download_file_response.content), file_buffer)
    client.files.delete_file_by_id(uploaded_file.id)


def testWithAsUserHeader():
    user_name: str = get_uuid()
    created_user: UserFull = client.users.create_user(
        user_name, is_platform_access_only=True
    )
    as_user_client: BoxClient = client.with_as_user_header(created_user.id)
    admin_user: UserFull = client.users.get_user_me()
    assert not to_string(admin_user.name) == user_name
    app_user: UserFull = as_user_client.users.get_user_me()
    assert to_string(app_user.name) == user_name
    client.users.delete_user_by_id(created_user.id)


def testWithSuppressedNotifications():
    new_client: BoxClient = client.with_suppressed_notifications()
    user: UserFull = new_client.users.get_user_me()
    assert not user.id == ''


def testWithExtraHeaders():
    user_name: str = get_uuid()
    created_user: UserFull = client.users.create_user(
        user_name, is_platform_access_only=True
    )
    as_user_client: BoxClient = client.with_extra_headers(
        extra_headers={'As-User': created_user.id}
    )
    admin_user: UserFull = client.users.get_user_me()
    assert not to_string(admin_user.name) == user_name
    app_user: UserFull = as_user_client.users.get_user_me()
    assert to_string(app_user.name) == user_name
    client.users.delete_user_by_id(created_user.id)


def testWithCustomBaseUrls():
    new_base_urls: BaseUrls = BaseUrls(
        base_url='https://box.com/',
        upload_url='https://box.com/',
        oauth_2_url='https://box.com/',
    )
    custom_base_client: BoxClient = client.with_custom_base_urls(new_base_urls)
    with pytest.raises(Exception):
        custom_base_client.users.get_user_me()
