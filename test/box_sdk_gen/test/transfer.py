from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.user_full import UserFull

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.managers.transfer import TransferOwnedFolderOwnedBy

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def testTransferUserContent():
    source_user_name: str = get_uuid()
    source_user: UserFull = client.users.create_user(
        source_user_name, is_platform_access_only=True
    )
    target_user: UserFull = client.users.get_user_me()
    transferred_folder: FolderFull = client.transfer.transfer_owned_folder(
        source_user.id, TransferOwnedFolderOwnedBy(id=target_user.id), notify=False
    )
    assert transferred_folder.owned_by.id == target_user.id
    client.folders.delete_folder_by_id(transferred_folder.id, recursive=True)
    client.users.delete_user_by_id(source_user.id, notify=False, force=True)
