from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.app_item_associations import AppItemAssociations

from box_sdk_gen.schemas.app_item_association import AppItemAssociation

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import get_env_var

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject


def testListFileAppItemAssocations():
    client: BoxClient = get_default_client_with_user_subject(get_env_var('USER_ID'))
    file_id: str = get_env_var('APP_ITEM_ASSOCIATION_FILE_ID')
    file_app_item_associations: AppItemAssociations = (
        client.app_item_associations.get_file_app_item_associations(file_id)
    )
    assert len(file_app_item_associations.entries) == 1
    association: AppItemAssociation = file_app_item_associations.entries[0]
    assert not association.id == ''
    assert to_string(association.app_item.application_type) == 'hubs'
    assert to_string(association.app_item.type) == 'app_item'
    assert to_string(association.item.type) == 'file'
    assert association.item.id == file_id
    file: FileFull = client.files.get_file_by_id(
        file_id, fields=['is_associated_with_app_item']
    )
    assert file.is_associated_with_app_item == True


def testListFolderAppItemAssocations():
    client: BoxClient = get_default_client_with_user_subject(get_env_var('USER_ID'))
    folder_id: str = get_env_var('APP_ITEM_ASSOCIATION_FOLDER_ID')
    folder_app_item_associations: AppItemAssociations = (
        client.app_item_associations.get_folder_app_item_associations(folder_id)
    )
    assert len(folder_app_item_associations.entries) == 1
    association: AppItemAssociation = folder_app_item_associations.entries[0]
    assert not association.id == ''
    assert to_string(association.app_item.application_type) == 'hubs'
    assert to_string(association.app_item.type) == 'app_item'
    assert to_string(association.item.type) == 'folder'
    assert association.item.id == folder_id
    folder: FolderFull = client.folders.get_folder_by_id(
        folder_id, fields=['is_associated_with_app_item']
    )
    assert folder.is_associated_with_app_item == True
