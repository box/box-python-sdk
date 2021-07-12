# coding: utf-8
from __future__ import unicode_literals, absolute_import
from .base_object import BaseObject


class CollaborationWhitelistEntry(BaseObject):
    """Represents a whitelisted email domain for enterprise collaboration."""
    _item_type = 'collaboration_whitelist_entry'

    def get_url(self, *args):
        """
        Gets the collaboration whitelist entries endpoint URL.

        :return:
            The collaboration whitelist entries endpoint URL.
        :rtype:
            `unicode`
        """
        return self._session.get_url('collaboration_whitelist_entries', self._object_id, *args)
