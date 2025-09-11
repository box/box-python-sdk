from typing import Optional

from box_sdk_gen.schemas.folder_base import FolderBaseTypeField

from box_sdk_gen.schemas.folder_base import FolderBase

from box_sdk_gen.box.errors import BoxSDKError


class FolderMini(FolderBase):
    def __init__(
        self,
        id: str,
        *,
        sequence_id: Optional[str] = None,
        name: Optional[str] = None,
        etag: Optional[str] = None,
        type: FolderBaseTypeField = FolderBaseTypeField.FOLDER,
        **kwargs
    ):
        """
                :param id: The unique identifier that represent a folder.

        The ID for any folder can be determined
        by visiting a folder in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/folders/123`
        the `folder_id` is `123`.
                :type id: str
                :param name: The name of the folder., defaults to None
                :type name: Optional[str], optional
                :param etag: The HTTP `etag` of this folder. This can be used within some API
        endpoints in the `If-Match` and `If-None-Match` headers to only
        perform changes on the folder if (no) changes have happened., defaults to None
                :type etag: Optional[str], optional
                :param type: The value will always be `folder`., defaults to FolderBaseTypeField.FOLDER
                :type type: FolderBaseTypeField, optional
        """
        super().__init__(id=id, etag=etag, type=type, **kwargs)
        self.sequence_id = sequence_id
        self.name = name
