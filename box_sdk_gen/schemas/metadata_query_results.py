from typing import Optional

from typing import List

from typing import Union

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.box.errors import BoxSDKError


class MetadataQueryResults(BaseObject):
    def __init__(
        self,
        *,
        entries: Optional[List[Union[FileFull, FolderFull]]] = None,
        limit: Optional[int] = None,
        next_marker: Optional[str] = None,
        **kwargs
    ):
        """
                :param entries: The mini representation of the files and folders that match the search
        terms.

        By default, this endpoint returns only the most basic info about the
        items. To get additional fields for each item, including any of the
        metadata, use the `fields` attribute in the query., defaults to None
                :type entries: Optional[List[Union[FileFull, FolderFull]]], optional
                :param limit: The limit that was used for this search. This will be the same as the
        `limit` query parameter unless that value exceeded the maximum value
        allowed., defaults to None
                :type limit: Optional[int], optional
                :param next_marker: The marker for the start of the next page of results., defaults to None
                :type next_marker: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.entries = entries
        self.limit = limit
        self.next_marker = next_marker
