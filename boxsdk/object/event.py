# coding: utf-8

from __future__ import unicode_literals

from boxsdk.object.base_object import BaseObject


class Event(BaseObject):
    """Represents a single Box event"""

    _item_type = 'event'

    @property
    def get_url(self, *args):
        """
        Base class override.
        Disallow this method for this subclass, should not access Event by event_id.
        """
        raise AttributeError("'Event' class has no method 'get_url'")
