from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class FolderReferenceTypeField(str, Enum):
    FOLDER = 'folder'


class FolderReference(BaseObject):
    _discriminator = 'type', {'folder'}

    def __init__(
        self,
        id: str,
        *,
        type: FolderReferenceTypeField = FolderReferenceTypeField.FOLDER,
        **kwargs
    ):
        """
        :param id: ID of the folder.
        :type id: str
        :param type: The value will always be `folder`., defaults to FolderReferenceTypeField.FOLDER
        :type type: FolderReferenceTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
