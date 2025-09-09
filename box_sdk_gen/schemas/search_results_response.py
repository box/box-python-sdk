from typing import Union

from box_sdk_gen.schemas.search_results import SearchResults

from box_sdk_gen.schemas.search_results_with_shared_links import (
    SearchResultsWithSharedLinks,
)

from box_sdk_gen.box.errors import BoxSDKError

SearchResultsResponse = Union[SearchResults, SearchResultsWithSharedLinks]
