from typing import Optional

from typing import Union

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.schemas.web_link import WebLink

from box_sdk_gen.box.errors import BoxSDKError


class SearchResultWithSharedLink(BaseObject):
    def __init__(
        self,
        *,
        accessible_via_shared_link: Optional[str] = None,
        item: Optional[Union[FileFull, FolderFull, WebLink]] = None,
        type: Optional[str] = None,
        **kwargs
    ):
        """
                :param accessible_via_shared_link: The optional shared link through which the user has access to this
        item. This value is only returned for items for which the user has
        recently accessed the file through a shared link. For all other
        items this value will return `null`., defaults to None
                :type accessible_via_shared_link: Optional[str], optional
                :param type: The result type. The value is always `search_result`., defaults to None
                :type type: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.accessible_via_shared_link = accessible_via_shared_link
        self.item = item
        self.type = type
