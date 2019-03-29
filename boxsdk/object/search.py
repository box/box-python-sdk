# coding: utf-8

from __future__ import unicode_literals, absolute_import

import json

from .base_endpoint import BaseEndpoint
from ..pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection
from ..util.api_call_decorator import api_call
from ..util.text_enum import TextEnum


class SearchScope(TextEnum):
    """Enum of possible serach scopes."""
    USER = 'user_content'
    ENTERPRISE = 'enterprise_content'


class TrashContent(TextEnum):
    """Enum of trash content values."""
    NONE = 'non_trashed_only'
    ONLY = 'trashed_only'


class MetadataSearchFilter(object):
    """
    Helper class to encapsulate a single search filter. A search filter can only search against one template,
    but can filter on many fields.
    See :class:`MetadataSearchFilters`.
    """
    def __init__(self, template_key, scope):
        """
        :param template_key:
            The key of the template to search on
        :type template_key:
            `unicode`
        :param scope:
            The scope of the template to search on
        :type scope:
            `unicode`
        """
        self._template_key = template_key
        self._scope = scope
        self._field_filters = {}

    def as_dict(self):
        """
        Returns a `dict` representation of this object

        :return:
            The `dict` representation
        :rtype:
            `dict`
        """
        return {
            'templateKey': self._template_key,
            'scope': self._scope,
            'filters': self._field_filters
        }

    def add_value_based_filter(self, field_key, value):
        """
        Add a value-based filter (used for token-based search on string fields, and exact match search on all other fields)

        :param field_key:
            The field key to filter on
        :type field_filter:
            `unicode`
        :param value:
            The value to use to filter
        :type value:
            `unicode`
        """
        self._field_filters.update({field_key: value})

    def add_range_filter(self, field_key, gt_value=None, lt_value=None):
        """
        Add a range filter (used for ranged searches on numbers and dates)

        :param field_key:
            The field key to filter on
        :type field_filter:
            `unicode`
        :param gt_value:
            The lower bound of the range filter (inclusive)
        :type gt_value:
            `unicode` or `int` or `float` or `long` or None
        :param lt_value:
            The upper bound of the range filter (inclusive)
        :type lt_value:
            `unicode` or `int` or `float` or `long` or None
        """
        range_part = {}
        if gt_value:
            range_part['gt'] = gt_value
        if lt_value:
            range_part['lt'] = lt_value
        if not range_part:
            raise ValueError('Should specify gt and/or lt')
        self._field_filters.update({field_key: range_part})


class MetadataSearchFilters(object):
    """
    Helper class to encapsulate a list of metadata search filter params (mdfilters API param)
    See https://developers.box.com/metadata-api/#search for more details
    """
    def __init__(self):
        self._filters = []

    def as_list(self):
        """
        Get a list of filters from this object to use as a parameter in the Search API

        :return:
            The list of filters
        :rtype:
            `list` of `dict`
        """
        return [metadata_filter.as_dict() for metadata_filter in self._filters]

    def add_filter(self, metadata_filter):
        """
        Add a filter to this object. Note that the API only supports one filter.

        :param metadata_filter:
            The filter to add
        :type metadata_filter:
            :class:`MetadataSearchFilter`
        """
        self._filters.append(metadata_filter)


class Search(BaseEndpoint):
    """Search Box for files and folders."""

    def get_url(self, *args):
        """
        Gets the search endpoint URL.

        :return:
            The search endpoint URL.
        :rtype:
            `unicode`
        """
        # pylint:disable=arguments-differ
        return super(Search, self).get_url('search')

    @staticmethod
    def start_metadata_filters():
        """
        Get a :class:`MetadataSearchFilters` that represents a set of metadata filters.

        :return:
            The new :class:`MetadataSearchFilters`
        :rtype:
            :class:`MetadataSearchFilters`
        """
        return MetadataSearchFilters()

    @staticmethod
    def make_single_metadata_filter(template_key, scope):
        """
        Make a single :class:`MetadataSearchFilter` that represents a filter on a template. It must be
        added to a :class:`MetadataSearchFilters`.

        :return:
            The new :class:`MetadataSearchFilter`
        :rtype:
            :class:`MetadataSearchFilter`
        """
        return MetadataSearchFilter(template_key, scope)

    @api_call
    # pylint: disable=too-many-arguments,too-many-locals,too-many-branches
    def query(
            self,
            query,
            limit=None,
            offset=0,
            ancestor_folders=None,
            file_extensions=None,
            metadata_filters=None,
            result_type=None,
            content_types=None,
            scope=None,
            created_at_range=None,
            updated_at_range=None,
            size_range=None,
            owner_users=None,
            trash_content=None,
            fields=None,
            sort=None,
            direction=None,
            **kwargs
    ):
        """
        Search Box for items matching the given query.

        :param query:
            The string to search for.
        :type query:
            `unicode`
        :param limit:
            The maximum number of items to return.
        :type limit:
            `int`
        :param offset:
            The search result at which to start the response.
        :type offset:
            `int`
        :param ancestor_folders:
            Folder ids to limit the search to.
        :type ancestor_folders:
            `Iterable` of :class:`Folder`
        :param file_extensions:
            File extensions to limit the search to.
        :type file_extensions:
            `iterable` of `unicode`
        :param metadata_filters:
            Filters used for metadata search
        :type metadata_filters:
            :class:`MetadataSearchFilters`
        :param result_type:
            Which type of result you want. Can be file or folder.
        :type result_type:
            `unicode`
        :param content_types:
            Which content types to search. Valid types include name, description, file_content, comments, and tags.
        :type content_types:
            `Iterable` of `unicode`
        :param scope:
            The scope of content to search over
        :type scope:
            `unicode` or None
        :param created_at_range:
            A tuple of the form (lower_bound, upper_bound) for the creation datetime of items to search.
        :type created_at_range:
            (`unicode` or None, `unicode` or None)
        :param updated_at_range:
            A tuple of the form (lower_bound, upper_bound) for the update datetime of items to search.
        :type updated_at_range:
            (`unicode` or None, `unicode` or None)
        :param size_range:
            A tuple of the form (lower_bound, upper_bound) for the size in bytes of items to search.
        :type size_range:
            (`int` or None, `int` or None)
        :param owner_users:
            Owner users to filter content by; only content belonging to these users will be returned.
        :type owner_users:
            `iterable` of :class:`User`
        :param trash_content:
            Whether to search trashed or non-trashed content.
        :type trash_content:
            `unicode` or None
        :param fields:
            Fields to include on the returned items.
        :type fields:
            `Iterable` of `unicode`
        :param sort:
            What to sort the search results by. Currently `modified_at`
        :type sort:
            `unicode` or None
        :param direction:
            The direction to display the sorted search results. Can be set to `DESC` for descending or `ASC` for ascending.
        :type direction:
            `unicode` or None
        :return:
            The collection of items that match the search query.
        :rtype:
            `Iterable` of :class:`Item`
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
            additional_params['created_at_range'] = '{},{}'.format(created_at_range[0] or '', created_at_range[1] or '')
        if updated_at_range is not None:
            additional_params['updated_at_range'] = '{},{}'.format(updated_at_range[0] or '', updated_at_range[1] or '')
        if size_range is not None:
            additional_params['size_range'] = '{},{}'.format(size_range[0] or '', size_range[1] or '')
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
