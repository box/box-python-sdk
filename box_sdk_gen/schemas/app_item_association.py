from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.file_base import FileBase

from box_sdk_gen.schemas.folder_base import FolderBase

from box_sdk_gen.schemas.web_link_base import WebLinkBase

from box_sdk_gen.schemas.app_item import AppItem

from box_sdk_gen.schemas.app_item_associated_item import AppItemAssociatedItem

from box_sdk_gen.box.errors import BoxSDKError


class AppItemAssociationTypeField(str, Enum):
    APP_ITEM_ASSOCIATION = 'app_item_association'


class AppItemAssociation(BaseObject):
    _discriminator = 'type', {'app_item_association'}

    def __init__(
        self,
        id: str,
        app_item: AppItem,
        item: AppItemAssociatedItem,
        *,
        type: AppItemAssociationTypeField = AppItemAssociationTypeField.APP_ITEM_ASSOCIATION,
        **kwargs
    ):
        """
        :param id: The unique identifier for this app item association.
        :type id: str
        :param type: The value will always be `app_item_association`., defaults to AppItemAssociationTypeField.APP_ITEM_ASSOCIATION
        :type type: AppItemAssociationTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.app_item = app_item
        self.item = item
        self.type = type
