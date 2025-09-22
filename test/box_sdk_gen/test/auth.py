import pytest

from box_sdk_gen.schemas.user_full import UserFull

from box_sdk_gen.schemas.files import Files

from box_sdk_gen.managers.uploads import UploadFileAttributes

from box_sdk_gen.managers.uploads import UploadFileAttributesParentField

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.access_token import AccessToken

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.managers.folders import CreateFolderParent

from box_sdk_gen.internal.utils import decode_base_64

from box_sdk_gen.internal.utils import get_env_var

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import buffer_equals

from box_sdk_gen.internal.utils import read_byte_stream

from box_sdk_gen.internal.utils import generate_byte_buffer

from box_sdk_gen.internal.utils import generate_byte_stream

from box_sdk_gen.internal.utils import decode_base_64_byte_stream

from box_sdk_gen.client import BoxClient

from box_sdk_gen.box.ccg_auth import BoxCCGAuth

from box_sdk_gen.box.ccg_auth import CCGConfig

from box_sdk_gen.box.developer_token_auth import BoxDeveloperTokenAuth

from box_sdk_gen.box.developer_token_auth import DeveloperTokenConfig

from box_sdk_gen.box.oauth import BoxOAuth

from box_sdk_gen.box.oauth import OAuthConfig

from box_sdk_gen.box.token_storage import InMemoryTokenStorage

from box_sdk_gen.box.jwt_auth import BoxJWTAuth

from box_sdk_gen.box.jwt_auth import JWTConfig


def test_jwt_auth():
    user_id: str = get_env_var('USER_ID')
    enterprise_id: str = get_env_var('ENTERPRISE_ID')
    jwt_config: JWTConfig = JWTConfig.from_config_json_string(
        decode_base_64(get_env_var('JWT_CONFIG_BASE_64'))
    )
    auth: BoxJWTAuth = BoxJWTAuth(config=jwt_config)
    user_auth: BoxJWTAuth = auth.with_user_subject(user_id)
    user_client: BoxClient = BoxClient(auth=user_auth)
    current_user: UserFull = user_client.users.get_user_me()
    assert current_user.id == user_id
    enterprise_auth: BoxJWTAuth = auth.with_enterprise_subject(enterprise_id)
    enterprise_client: BoxClient = BoxClient(auth=enterprise_auth)
    new_user: UserFull = enterprise_client.users.get_user_me(fields=['enterprise'])
    assert not new_user.enterprise == None
    assert new_user.enterprise.id == enterprise_id
    assert not new_user.id == user_id


def test_jwt_auth_downscope():
    jwt_config: JWTConfig = JWTConfig.from_config_json_string(
        decode_base_64(get_env_var('JWT_CONFIG_BASE_64'))
    )
    auth: BoxJWTAuth = BoxJWTAuth(config=jwt_config)
    parent_client: BoxClient = BoxClient(auth=auth)
    uploaded_files: Files = parent_client.uploads.upload_file(
        UploadFileAttributes(
            name=get_uuid(), parent=UploadFileAttributesParentField(id='0')
        ),
        generate_byte_stream(1024 * 1024),
    )
    file: FileFull = uploaded_files.entries[0]
    resource_path: str = ''.join(['https://api.box.com/2.0/files/', file.id])
    downscoped_token: AccessToken = auth.downscope_token(
        ['item_rename', 'item_preview'], resource=resource_path
    )
    assert not downscoped_token.access_token == None
    downscoped_client: BoxClient = BoxClient(
        auth=BoxDeveloperTokenAuth(token=downscoped_token.access_token)
    )
    downscoped_client.files.update_file_by_id(file.id, name=get_uuid())
    with pytest.raises(Exception):
        downscoped_client.files.delete_file_by_id(file.id)
    parent_client.files.delete_file_by_id(file.id)


def test_jwt_downscope_token_succeeds_if_no_token_available():
    jwt_config: JWTConfig = JWTConfig.from_config_json_string(
        decode_base_64(get_env_var('JWT_CONFIG_BASE_64'))
    )
    auth: BoxJWTAuth = BoxJWTAuth(config=jwt_config)
    downscoped_token: AccessToken = auth.downscope_token(['root_readonly'])
    assert not downscoped_token.access_token == None
    downscoped_client: BoxClient = BoxClient(
        auth=BoxDeveloperTokenAuth(token=downscoped_token.access_token)
    )
    with pytest.raises(Exception):
        downscoped_client.uploads.upload_file(
            UploadFileAttributes(
                name=get_uuid(), parent=UploadFileAttributesParentField(id='0')
            ),
            generate_byte_stream(1024 * 1024),
        )


def test_jwt_auth_revoke():
    jwt_config: JWTConfig = JWTConfig.from_config_json_string(
        decode_base_64(get_env_var('JWT_CONFIG_BASE_64'))
    )
    auth: BoxJWTAuth = BoxJWTAuth(config=jwt_config)
    token_from_storage_before_revoke: AccessToken = auth.retrieve_token()
    assert not token_from_storage_before_revoke == None
    auth.revoke_token()
    token_from_storage_after_revoke: AccessToken = auth.retrieve_token()
    assert (
        not token_from_storage_before_revoke.access_token
        == token_from_storage_after_revoke.access_token
    )


def test_oauth_auth_authorizeUrl():
    config: OAuthConfig = OAuthConfig(
        client_id='OAUTH_CLIENT_ID', client_secret='OAUTH_CLIENT_SECRET'
    )
    auth: BoxOAuth = BoxOAuth(config=config)
    auth_url: str = auth.get_authorize_url()
    assert (
        auth_url
        == 'https://account.box.com/api/oauth2/authorize?client_id=OAUTH_CLIENT_ID&response_type=code'
        or auth_url
        == 'https://account.box.com/api/oauth2/authorize?response_type=code&client_id=OAUTH_CLIENT_ID'
    )


def test_oauth_downscope_token_succeeds_if_no_token_available():
    config: OAuthConfig = OAuthConfig(
        client_id=get_env_var('CLIENT_ID'), client_secret=get_env_var('CLIENT_SECRET')
    )
    auth: BoxOAuth = BoxOAuth(config=config)
    resource_path: str = ''.join(['https://api.box.com/2.0/files/12345'])
    with pytest.raises(Exception):
        auth.downscope_token(['item_rename', 'item_preview'], resource=resource_path)


def test_ccg_auth():
    user_id: str = get_env_var('USER_ID')
    enterprise_id: str = get_env_var('ENTERPRISE_ID')
    ccg_config: CCGConfig = CCGConfig(
        client_id=get_env_var('CLIENT_ID'),
        client_secret=get_env_var('CLIENT_SECRET'),
        enterprise_id=enterprise_id,
        user_id=user_id,
    )
    auth: BoxCCGAuth = BoxCCGAuth(config=ccg_config)
    user_auth: BoxCCGAuth = auth.with_user_subject(user_id)
    user_client: BoxClient = BoxClient(auth=user_auth)
    current_user: UserFull = user_client.users.get_user_me()
    assert current_user.id == user_id
    enterprise_auth: BoxCCGAuth = auth.with_enterprise_subject(enterprise_id)
    enterprise_client: BoxClient = BoxClient(auth=enterprise_auth)
    new_user: UserFull = enterprise_client.users.get_user_me(fields=['enterprise'])
    assert not new_user.enterprise == None
    assert new_user.enterprise.id == enterprise_id
    assert not new_user.id == user_id


def test_ccg_auth_downscope():
    ccg_config: CCGConfig = CCGConfig(
        client_id=get_env_var('CLIENT_ID'),
        client_secret=get_env_var('CLIENT_SECRET'),
        user_id=get_env_var('USER_ID'),
    )
    auth: BoxCCGAuth = BoxCCGAuth(config=ccg_config)
    parent_client: BoxClient = BoxClient(auth=auth)
    folder: FolderFull = parent_client.folders.create_folder(
        get_uuid(), CreateFolderParent(id='0')
    )
    resource_path: str = ''.join(['https://api.box.com/2.0/folders/', folder.id])
    downscoped_token: AccessToken = auth.downscope_token(
        ['item_rename', 'item_preview'], resource=resource_path
    )
    assert not downscoped_token.access_token == None
    downscoped_client: BoxClient = BoxClient(
        auth=BoxDeveloperTokenAuth(token=downscoped_token.access_token)
    )
    downscoped_client.folders.update_folder_by_id(folder.id, name=get_uuid())
    with pytest.raises(Exception):
        downscoped_client.folders.delete_folder_by_id(folder.id)
    parent_client.folders.delete_folder_by_id(folder.id)


def test_ccg_downscope_token_succeeds_if_no_token_available():
    ccg_config: CCGConfig = CCGConfig(
        client_id=get_env_var('CLIENT_ID'),
        client_secret=get_env_var('CLIENT_SECRET'),
        user_id=get_env_var('USER_ID'),
    )
    auth: BoxCCGAuth = BoxCCGAuth(config=ccg_config)
    downscoped_token: AccessToken = auth.downscope_token(['root_readonly'])
    assert not downscoped_token.access_token == None
    downscoped_client: BoxClient = BoxClient(
        auth=BoxDeveloperTokenAuth(token=downscoped_token.access_token)
    )
    with pytest.raises(Exception):
        downscoped_client.uploads.upload_file(
            UploadFileAttributes(
                name=get_uuid(), parent=UploadFileAttributesParentField(id='0')
            ),
            generate_byte_stream(1024 * 1024),
        )


def test_ccg_auth_revoke():
    ccg_config: CCGConfig = CCGConfig(
        client_id=get_env_var('CLIENT_ID'),
        client_secret=get_env_var('CLIENT_SECRET'),
        user_id=get_env_var('USER_ID'),
    )
    auth: BoxCCGAuth = BoxCCGAuth(config=ccg_config)
    token_from_storage_before_revoke: AccessToken = auth.retrieve_token()
    assert not token_from_storage_before_revoke == None
    auth.revoke_token()
    token_from_storage_after_revoke: AccessToken = auth.retrieve_token()
    assert (
        not token_from_storage_before_revoke.access_token
        == token_from_storage_after_revoke.access_token
    )


def test_developer_downscope_token_succeeds_if_no_token_available():
    developer_token_config: DeveloperTokenConfig = DeveloperTokenConfig(
        client_id=get_env_var('CLIENT_ID'), client_secret=get_env_var('CLIENT_SECRET')
    )
    auth: BoxDeveloperTokenAuth = BoxDeveloperTokenAuth(
        token='', config=developer_token_config
    )
    resource_path: str = ''.join(['https://api.box.com/2.0/folders/12345'])
    with pytest.raises(Exception):
        auth.downscope_token(['item_rename', 'item_preview'], resource=resource_path)


def get_access_token() -> AccessToken:
    user_id: str = get_env_var('USER_ID')
    enterprise_id: str = get_env_var('ENTERPRISE_ID')
    ccg_config: CCGConfig = CCGConfig(
        client_id=get_env_var('CLIENT_ID'),
        client_secret=get_env_var('CLIENT_SECRET'),
        enterprise_id=enterprise_id,
        user_id=user_id,
    )
    auth: BoxCCGAuth = BoxCCGAuth(config=ccg_config)
    auth_user: BoxCCGAuth = auth.with_user_subject(user_id)
    return auth_user.retrieve_token()


def test_developer_token_auth_revoke():
    developer_token_config: DeveloperTokenConfig = DeveloperTokenConfig(
        client_id=get_env_var('CLIENT_ID'), client_secret=get_env_var('CLIENT_SECRET')
    )
    token: AccessToken = get_access_token()
    auth: BoxDeveloperTokenAuth = BoxDeveloperTokenAuth(
        token=token.access_token, config=developer_token_config
    )
    token_from_storage_before_revoke: AccessToken = auth.retrieve_token()
    assert not token_from_storage_before_revoke == None
    auth.revoke_token()
    with pytest.raises(Exception):
        auth.retrieve_token()


def test_developer_token_auth_downscope():
    developer_token_config: DeveloperTokenConfig = DeveloperTokenConfig(
        client_id=get_env_var('CLIENT_ID'), client_secret=get_env_var('CLIENT_SECRET')
    )
    token: AccessToken = get_access_token()
    auth: BoxDeveloperTokenAuth = BoxDeveloperTokenAuth(
        token=token.access_token, config=developer_token_config
    )
    parent_client: BoxClient = BoxClient(auth=auth)
    folder: FolderFull = parent_client.folders.create_folder(
        get_uuid(), CreateFolderParent(id='0')
    )
    resource_path: str = ''.join(['https://api.box.com/2.0/folders/', folder.id])
    downscoped_token: AccessToken = auth.downscope_token(
        ['item_rename', 'item_preview'], resource=resource_path
    )
    assert not downscoped_token.access_token == None
    downscoped_client: BoxClient = BoxClient(
        auth=BoxDeveloperTokenAuth(token=downscoped_token.access_token)
    )
    downscoped_client.folders.update_folder_by_id(folder.id, name=get_uuid())
    with pytest.raises(Exception):
        downscoped_client.folders.delete_folder_by_id(folder.id)
    parent_client.folders.delete_folder_by_id(folder.id)


def test_developer_token_auth():
    user_id: str = get_env_var('USER_ID')
    token: AccessToken = get_access_token()
    dev_auth: BoxDeveloperTokenAuth = BoxDeveloperTokenAuth(token=token.access_token)
    client: BoxClient = BoxClient(auth=dev_auth)
    current_user: UserFull = client.users.get_user_me()
    assert current_user.id == user_id


def test_oauth_auth_revoke():
    token: AccessToken = get_access_token()
    token_storage: InMemoryTokenStorage = InMemoryTokenStorage(token=token)
    config: OAuthConfig = OAuthConfig(
        client_id=get_env_var('CLIENT_ID'),
        client_secret=get_env_var('CLIENT_SECRET'),
        token_storage=token_storage,
    )
    auth: BoxOAuth = BoxOAuth(config=config)
    client: BoxClient = BoxClient(auth=auth)
    client.users.get_user_me()
    auth.revoke_token()
    with pytest.raises(Exception):
        client.users.get_user_me()


def test_oauth_auth_downscope():
    token: AccessToken = get_access_token()
    token_storage: InMemoryTokenStorage = InMemoryTokenStorage(token=token)
    config: OAuthConfig = OAuthConfig(
        client_id=get_env_var('CLIENT_ID'),
        client_secret=get_env_var('CLIENT_SECRET'),
        token_storage=token_storage,
    )
    auth: BoxOAuth = BoxOAuth(config=config)
    parent_client: BoxClient = BoxClient(auth=auth)
    uploaded_files: Files = parent_client.uploads.upload_file(
        UploadFileAttributes(
            name=get_uuid(), parent=UploadFileAttributesParentField(id='0')
        ),
        generate_byte_stream(1024 * 1024),
    )
    file: FileFull = uploaded_files.entries[0]
    resource_path: str = ''.join(['https://api.box.com/2.0/files/', file.id])
    downscoped_token: AccessToken = auth.downscope_token(
        ['item_rename', 'item_preview'], resource=resource_path
    )
    assert not downscoped_token.access_token == None
    downscoped_client: BoxClient = BoxClient(
        auth=BoxDeveloperTokenAuth(token=downscoped_token.access_token)
    )
    downscoped_client.files.update_file_by_id(file.id, name=get_uuid())
    with pytest.raises(Exception):
        downscoped_client.files.delete_file_by_id(file.id)
    parent_client.files.delete_file_by_id(file.id)
