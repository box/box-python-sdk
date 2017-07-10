# coding: utf-8

from __future__ import unicode_literals, absolute_import

from .base_endpoint import BaseEndpoint
from .base_api_json_object import BaseAPIJSONObject


class RecentItem(BaseEndpoint, BaseAPIJSONObject):
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
        super(RecentItem, self).__init__(session=session, response_object=response_object)

    @property
    def item(self):
        """
        Returns the Box Item which this recent item references.

        :rtype:
            :class:`Item`
        """
        item = self._response_object['item']
        return self.translator.translate(item['type'])(
            session=self._session,
            object_id=item['id'],
            response_object=item,
        )

    def get_url(self, *args):
        """Base class override."""
        # pylint:disable=arguments-differ
        return super(RecentItem, self).get_url('recent_items', *args)
