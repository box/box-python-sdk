# coding: utf-8

from __future__ import unicode_literals

from boxsdk.config import API
from .base_endpoint import BaseEndpoint
from .translator import Translator


class Search(BaseEndpoint):
    """Search Box for files and folders."""

    def search(self, query, limit, offset, ancestor_folders=None, file_extensions=None):
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
            `list` of `unicode`
        :param file_extensions:
            File extensions to limit the search to.
        :type file_extensions:
            `list` of `unicode`
        :return:
            A list of items that match the search query.
        :rtype:
            `list` of :class:`Item`
        """
        url = '{0}/search'.format(API.BASE_API_URL)
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
            params.update({
                'file_extensions': ','.join(file_extensions)
            })
        box_response = self._session.get(url, params=params)
        response = box_response.json()
        return [Translator().translate(item['type'])(self._session, item['id'], item) for item in response['entries']]
