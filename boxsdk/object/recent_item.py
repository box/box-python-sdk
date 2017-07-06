# coding: utf-8

from __future__ import unicode_literals, absolute_import

from .base_api_json_object import BaseAPIJSONObject


class RecentItem(BaseAPIJSONObject):
    """Represents a single recent item accessed by a Box user."""

    _item_type = 'recent_item'

    def __init__(self, session, response_object=None):
        """
        :param session:
            The Box session used to make requests.
        :type session:
            :class:`BoxSession`
        :param response_object:
            A JSON object representing the object returned from a Box API request.
        :type response_object:
            `dict`
        """
        super(RecentItem, self).__init__(response_object=response_object)
        self._session = session

    @property
    def translator(self):
        """The translator used for translating Box API JSON responses into `BaseAPIJSONObject` smart objects.

        :rtype:   :class:`Translator`
        """
        return self._session.translator

    @property
    def item(self):
        """
        Returns the Box Item which this recent item references.

        :rtype:
            :class:`Item`
        """
        item = self.response_object['item']
        return self.translator.translate(item['type'])(self._session, item['id'], item)
