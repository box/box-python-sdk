from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class FolderReferenceV2025R0TypeField(str, Enum):
    FOLDER = 'folder'


class FolderReferenceV2025R0(BaseObject):
    _discriminator = 'type', {'folder'}

    def __init__(
        self,
        id: str,
        *,
        type: FolderReferenceV2025R0TypeField = FolderReferenceV2025R0TypeField.FOLDER,
        **kwargs
    ):
        """
        :param id: ID of the folder.
        :type id: str
        :param type: The value will always be `folder`., defaults to FolderReferenceV2025R0TypeField.FOLDER
        :type type: FolderReferenceV2025R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
