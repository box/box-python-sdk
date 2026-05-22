from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class FolderReferenceV2026R0TypeField(str, Enum):
    FOLDER = 'folder'


class FolderReferenceV2026R0(BaseObject):
    _discriminator = 'type', {'folder'}

    def __init__(
        self,
        id: str,
        *,
        type: FolderReferenceV2026R0TypeField = FolderReferenceV2026R0TypeField.FOLDER,
        **kwargs
    ):
        """
        :param id: ID of the folder.
        :type id: str
        :param type: The value will always be `folder`., defaults to FolderReferenceV2026R0TypeField.FOLDER
        :type type: FolderReferenceV2026R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
