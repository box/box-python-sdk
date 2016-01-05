# coding: utf-8

from __future__ import unicode_literals

import json

from .base_endpoint import BaseEndpoint
from boxsdk.util.translator import Translator


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

    def search(
            self,
            query,
            limit=100,
            offset=0,
            ancestor_folders=None,
            file_extensions=None,
            metadata_filters=None,
            result_type=None,
            content_types=None,
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
        :return:
            A list of items that match the search query.
        :rtype:
            `list` of :class:`Item`
        """
        url = self.get_url()
        params = {
            'query': query,
            'limit': limit,
            'offset': offset,
        }
        if ancestor_folders:
            params.update({
                'ancestor_folder_ids': ','.join([folder.object_id for folder in ancestor_folders])
            })
        if file_extensions:
            params.update({'file_extensions': ','.join(file_extensions)})
        if metadata_filters:
            params.update({'mdfilters': json.dumps(metadata_filters.as_list())})
        if content_types:
            params.update({'content_types': ','.join(content_types)})
        if result_type:
            params.update({'type': result_type})
        params.update(kwargs)
        box_response = self._session.get(url, params=params)
        response = box_response.json()
        return [Translator().translate(item['type'])(self._session, item['id'], item) for item in response['entries']]
