from enum import Enum

from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.schemas.web_link import WebLink

from box_sdk_gen.schemas.search_result_item import SearchResultItem

from box_sdk_gen.box.errors import BoxSDKError


class SearchResultsTypeField(str, Enum):
    SEARCH_RESULTS_ITEMS = 'search_results_items'


class SearchResults(BaseObject):
    _discriminator = 'type', {'search_results_items'}

    def __init__(
        self,
        *,
        total_count: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        type: SearchResultsTypeField = SearchResultsTypeField.SEARCH_RESULTS_ITEMS,
        entries: Optional[List[SearchResultItem]] = None,
        **kwargs
    ):
        """
                :param total_count: One greater than the offset of the last entry in the search results.
        The total number of entries in the collection may be less than
        `total_count`., defaults to None
                :type total_count: Optional[int], optional
                :param limit: The limit that was used for this search. This will be the same as the
        `limit` query parameter unless that value exceeded the maximum value
        allowed., defaults to None
                :type limit: Optional[int], optional
                :param offset: The 0-based offset of the first entry in this set. This will be the same
        as the `offset` query parameter used., defaults to None
                :type offset: Optional[int], optional
                :param type: Specifies the response as search result items without shared links., defaults to SearchResultsTypeField.SEARCH_RESULTS_ITEMS
                :type type: SearchResultsTypeField, optional
                :param entries: The search results for the query provided., defaults to None
                :type entries: Optional[List[SearchResultItem]], optional
        """
        super().__init__(**kwargs)
        self.total_count = total_count
        self.limit = limit
        self.offset = offset
        self.type = type
        self.entries = entries
