# coding: utf-8

from __future__ import unicode_literals, absolute_import

from .base_endpoint import BaseEndpoint
from .base_api_json_object import BaseAPIJSONObject


class RecentItem(BaseEndpoint, BaseAPIJSONObject):
    """Represents a single recent item accessed by a Box user."""

    _item_type = 'recent_item'

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
