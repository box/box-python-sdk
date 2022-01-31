# coding: utf-8

import json
from typing import Optional, List, Any, Iterable, TYPE_CHECKING, Tuple, Union
from .base_endpoint import BaseEndpoint
from ..pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection
from ..util.api_call_decorator import api_call
from ..util.deprecation_decorator import deprecated_param
from ..util.text_enum import TextEnum

if TYPE_CHECKING:
    from boxsdk.object.folder import Folder
    from boxsdk.object.user import User
    from boxsdk.object.item import Item
    from boxsdk.pagination.box_object_collection import BoxObjectCollection


class SearchScope(TextEnum):
    """Enum of possible serach scopes."""
    USER = 'user_content'
    ENTERPRISE = 'enterprise_content'


class TrashContent(TextEnum):
    """Enum of trash content values."""
    NONE = 'non_trashed_only'
    ONLY = 'trashed_only'


class MetadataSearchFilter:
    """
    Helper class to encapsulate a single search filter. A search filter can only search against one template,
    but can filter on many fields.
    See :class:`MetadataSearchFilters`.
    """
    def __init__(self, template_key: str, scope: str):
        """
        :param template_key:
            The key of the template to search on
        :param scope:
            The scope of the template to search on
        """
        self._template_key = template_key
        self._scope = scope
        self._field_filters = {}

    def as_dict(self) -> dict:
        """
        Returns a `dict` representation of this object

        :return:
            The `dict` representation
        """
        return {
            'templateKey': self._template_key,
            'scope': self._scope,
            'filters': self._field_filters
        }

    def add_value_based_filter(self, field_key: str, value: str) -> None:
        """
        Add a value-based filter (used for token-based search on string fields, and exact match search on all other fields)

        :param field_key:
            The field key to filter on
        :param value:
            The value to use to filter
        """
        self._field_filters.update({field_key: value})

    def add_range_filter(
            self,
            field_key: str,
            gt_value: Union[str, int, float] = None,
            lt_value: Union[str, int, float] = None
    ) -> None:
        """
        Add a range filter (used for ranged searches on numbers and dates)

        :param field_key:
            The field key to filter on
        :param gt_value:
            The lower bound of the range filter (inclusive)
        :param lt_value:
            The upper bound of the range filter (inclusive)
        """
        range_part = {}
        if gt_value:
            range_part['gt'] = gt_value
        if lt_value:
            range_part['lt'] = lt_value
        if not range_part:
            raise ValueError('Should specify gt and/or lt')
        self._field_filters.update({field_key: range_part})


class MetadataSearchFilters:
    """
    Helper class to encapsulate a list of metadata search filter params (mdfilters API param)
    See https://developers.box.com/metadata-api/#search for more details
    """
    def __init__(self):
        self._filters = []

    def as_list(self) -> List[dict]:
        """
        Get a list of filters from this object to use as a parameter in the Search API

        :return:
            The list of filters
        """
        return [metadata_filter.as_dict() for metadata_filter in self._filters]

    def add_filter(self, metadata_filter: MetadataSearchFilter) -> None:
        """
        Add a filter to this object. Note that the API only supports one filter.

        :param metadata_filter:
            The filter to add
        """
        self._filters.append(metadata_filter)


class Search(BaseEndpoint):
    """Search Box for files and folders."""

    def get_url(self, *args: Any) -> str:
        """
        Gets the search endpoint URL.

        :return:
            The search endpoint URL.
        """
        return super().get_url('search', *args)

    @staticmethod
    def start_metadata_filters() -> MetadataSearchFilters:
        """
        Get a :class:`MetadataSearchFilters` that represents a set of metadata filters.

        :return:
            The new :class:`MetadataSearchFilters`
        """
        return MetadataSearchFilters()

    @staticmethod
    def make_single_metadata_filter(template_key: str, scope: str) -> MetadataSearchFilter:
        """
        Make a single :class:`MetadataSearchFilter` that represents a filter on a template. It must be
        added to a :class:`MetadataSearchFilters`.
        :param template_key:
            The key of the template to filter on
        :param scope:
            The scope of the template to filter on
        :return:
            The new :class:`MetadataSearchFilter`
        """
        return MetadataSearchFilter(template_key, scope)

    @api_call
    # pylint: disable=too-many-arguments,too-many-locals,too-many-branches
    def query(
            self,
            query: str,
            limit: int = None,
            offset: int = 0,
            ancestor_folders: Iterable['Folder'] = None,
            file_extensions: Iterable[str] = None,
            metadata_filters: MetadataSearchFilters = None,
            result_type: str = None,
            content_types: Iterable[str] = None,
            scope: Optional[str] = None,
            created_at_range: Tuple[Optional[str], Optional[str]] = None,
            updated_at_range: Tuple[Optional[str], Optional[str]] = None,
            size_range: Tuple[Optional[int], Optional[int]] = None,
            owner_users: Iterable['User'] = None,
            trash_content: Optional[str] = None,
            fields: Iterable[str] = None,
            sort: Optional[str] = None,
            direction: Optional[str] = None,
            **kwargs: Any
    ) -> Iterable['Item']:
        """
        Search Box for items matching the given query.

        :param query:
            The string to search for.
        :param limit:
            The maximum number of items to return.
        :param offset:
            The search result at which to start the response.
        :param ancestor_folders:
            Folder ids to limit the search to.
        :param file_extensions:
            File extensions to limit the search to.
        :param metadata_filters:
            Filters used for metadata search
        :param result_type:
            Which type of result you want. Can be file or folder.
        :param content_types:
            Which content types to search. Valid types include name, description, file_content, comments, and tags.
        :param scope:
            The scope of content to search over
        :param created_at_range:
            A tuple of the form (lower_bound, upper_bound) for the creation datetime of items to search.
        :param updated_at_range:
            A tuple of the form (lower_bound, upper_bound) for the update datetime of items to search.
        :param size_range:
            A tuple of the form (lower_bound, upper_bound) for the size in bytes of items to search.
        :param owner_users:
            Owner users to filter content by; only content belonging to these users will be returned.
        :param trash_content:
            Whether to search trashed or non-trashed content.
        :param fields:
            Fields to include on the returned items.
        :param sort:
            What to sort the search results by. Currently `modified_at`
        :param direction:
            The direction to display the sorted search results. Can be set to `DESC` for descending or `ASC` for ascending.
        :return:
            The collection of items that match the search query.
        """
        url = self.get_url()
        additional_params = {'query': query}
        if ancestor_folders is not None:
            additional_params['ancestor_folder_ids'] = ','.join([folder.object_id for folder in ancestor_folders])
        if file_extensions is not None:
            additional_params['file_extensions'] = ','.join(file_extensions)
        if metadata_filters is not None:
            additional_params['mdfilters'] = json.dumps(metadata_filters.as_list())
        if content_types is not None:
            additional_params['content_types'] = ','.join(content_types)
        if result_type is not None:
            additional_params['type'] = result_type
        if scope is not None:
            additional_params['scope'] = scope
        if created_at_range is not None:
            additional_params['created_at_range'] = f'{created_at_range[0] or ""},{created_at_range[1] or ""}'
        if updated_at_range is not None:
            additional_params['updated_at_range'] = f'{updated_at_range[0] or ""},{updated_at_range[1] or ""}'
        if size_range is not None:
            additional_params['size_range'] = f'{size_range[0] or ""},{size_range[1] or ""}'
        if owner_users is not None:
            additional_params['owner_user_ids'] = ','.join([user.object_id for user in owner_users])
        if trash_content is not None:
            additional_params['trash_content'] = trash_content
        if sort is not None:
            additional_params['sort'] = sort
        if direction is not None:
            additional_params['direction'] = direction

        additional_params.update(kwargs)

        return LimitOffsetBasedObjectCollection(
            self._session,
            url,
            limit=limit,
            offset=offset,
            fields=fields,
            additional_params=additional_params,
            return_full_pages=False,
        )

    @deprecated_param(name="use_index", position=5, message="Parameter will be ignored. See docs for details.")
    @api_call
    def metadata_query(
            self,
            from_template: str,
            ancestor_folder_id: str,
            query: Optional[str] = None,
            query_params: Optional[dict] = None,
            use_index: Optional[str] = None,
            order_by: List[dict] = None,
            marker: Optional[str] = None,
            limit: int = None,
            fields: Iterable[Optional[str]] = None
    ) -> 'BoxObjectCollection':
        # pylint:disable=unused-argument
        """Query Box items by their metadata.

        :param from_template:
            The template used in the query. Must be in the form scope.templateKey.
        :param ancestor_folder_id:
            The folder_id to which to restrain the query
        :param query:
            The logical expression of the query
        :param query_params:
            Required if query present. The arguments for the query.
        :param use_index is deprecated
        :param order_by:
            The field_key(s) to order on and the corresponding direction(s)
        :param marker:
            The marker to use for requesting the next page
        :param limit:
            Max results to return for a single request (0-100 inclusive)
        :param fields:
            List of fields to request
        :returns:
            An iterator of the item search results
        """
        url = super().get_url('metadata_queries/execute_read')
        data = {
            'from': from_template,
            'ancestor_folder_id': ancestor_folder_id
        }
        if query is not None:
            data['query'] = query
        if query_params is not None:
            data['query_params'] = query_params
        if order_by is not None:
            data['order_by'] = order_by

        return MarkerBasedObjectCollection(
            session=self._session,
            url=url,
            limit=limit,
            marker=marker,
            fields=fields,
            additional_params=data,
            return_full_pages=False,
            use_post=True
        )

    @api_call
    # pylint: disable=too-many-arguments,too-many-locals,too-many-branches
    def query_with_shared_links(
            self,
            query: str,
            limit: int = None,
            offset: int = 0,
            ancestor_folders: Iterable['Folder'] = None,
            file_extensions: Iterable[str] = None,
            metadata_filters: MetadataSearchFilters = None,
            result_type: str = None,
            content_types: Iterable[str] = None,
            scope: Optional[str] = None,
            created_at_range: Tuple[Optional[str], Optional[str]] = None,
            updated_at_range: Tuple[Optional[str], Optional[str]] = None,
            size_range: Tuple[Optional[int], Optional[int]] = None,
            owner_users: Iterable['User'] = None,
            trash_content: Optional[str] = None,
            fields: Iterable[str] = None,
            sort: Optional[str] = None,
            direction: Optional[str] = None,
            **kwargs: Any
    ) -> Iterable['Item']:
        """
        Search Box for items matching the given query. May also include items that are only accessible via recently used shared links.

        :param query:
            The string to search for.
        :param limit:
            The maximum number of items to return.
        :param offset:
            The search result at which to start the response.
        :param ancestor_folders:
            Folder ids to limit the search to.
        :param file_extensions:
            File extensions to limit the search to.
        :param metadata_filters:
            Filters used for metadata search
        :param result_type:
            Which type of result you want. Can be file or folder.
        :param content_types:
            Which content types to search. Valid types include name, description, file_content, comments, and tags.
        :param scope:
            The scope of content to search over
        :param created_at_range:
            A tuple of the form (lower_bound, upper_bound) for the creation datetime of items to search.
        :param updated_at_range:
            A tuple of the form (lower_bound, upper_bound) for the update datetime of items to search.
        :param size_range:
            A tuple of the form (lower_bound, upper_bound) for the size in bytes of items to search.
        :param owner_users:
            Owner users to filter content by; only content belonging to these users will be returned.
        :param trash_content:
            Whether to search trashed or non-trashed content.
        :param fields:
            Fields to include on the returned items.
        :param sort:
            What to sort the search results by. Currently `modified_at`
        :param direction:
            The direction to display the sorted search results. Can be set to `DESC` for descending or `ASC` for ascending.
        :return:
            The collection of items that match the search query.
        """
        url = self.get_url()
        additional_params = {'query': query, 'include_recent_shared_links': True}
        if ancestor_folders is not None:
            additional_params['ancestor_folder_ids'] = ','.join([folder.object_id for folder in ancestor_folders])
        if file_extensions is not None:
            additional_params['file_extensions'] = ','.join(file_extensions)
        if metadata_filters is not None:
            additional_params['mdfilters'] = json.dumps(metadata_filters.as_list())
        if content_types is not None:
            additional_params['content_types'] = ','.join(content_types)
        if result_type is not None:
            additional_params['type'] = result_type
        if scope is not None:
            additional_params['scope'] = scope
        if created_at_range is not None:
            additional_params['created_at_range'] = f'{created_at_range[0] or ""},{created_at_range[1] or ""}'
        if updated_at_range is not None:
            additional_params['updated_at_range'] = f'{updated_at_range[0] or ""},{updated_at_range[1] or ""}'
        if size_range is not None:
            additional_params['size_range'] = f'{size_range[0] or ""},{size_range[1] or ""}'
        if owner_users is not None:
            additional_params['owner_user_ids'] = ','.join([user.object_id for user in owner_users])
        if trash_content is not None:
            additional_params['trash_content'] = trash_content
        if sort is not None:
            additional_params['sort'] = sort
        if direction is not None:
            additional_params['direction'] = direction

        additional_params.update(kwargs)

        return LimitOffsetBasedObjectCollection(
            self._session,
            url,
            limit=limit,
            offset=offset,
            fields=fields,
            additional_params=additional_params,
            return_full_pages=False,
        )
