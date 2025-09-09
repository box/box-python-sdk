from enum import Enum

from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.search_result_with_shared_link import (
    SearchResultWithSharedLink,
)

from box_sdk_gen.box.errors import BoxSDKError


class SearchResultsWithSharedLinksTypeField(str, Enum):
    SEARCH_RESULTS_WITH_SHARED_LINKS = 'search_results_with_shared_links'


class SearchResultsWithSharedLinks(BaseObject):
    _discriminator = 'type', {'search_results_with_shared_links'}

    def __init__(
        self,
        *,
        total_count: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        type: SearchResultsWithSharedLinksTypeField = SearchResultsWithSharedLinksTypeField.SEARCH_RESULTS_WITH_SHARED_LINKS,
        entries: Optional[List[SearchResultWithSharedLink]] = None,
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
                :param type: Specifies the response as search result items with shared links., defaults to SearchResultsWithSharedLinksTypeField.SEARCH_RESULTS_WITH_SHARED_LINKS
                :type type: SearchResultsWithSharedLinksTypeField, optional
                :param entries: The search results for the query provided, including the
        additional information about any shared links through
        which the item has been shared with the user., defaults to None
                :type entries: Optional[List[SearchResultWithSharedLink]], optional
        """
        super().__init__(**kwargs)
        self.total_count = total_count
        self.limit = limit
        self.offset = offset
        self.type = type
        self.entries = entries
