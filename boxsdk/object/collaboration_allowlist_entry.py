# coding: utf-8
from typing import Any

from .collaboration_whitelist_entry import CollaborationWhitelistEntry


class CollaborationAllowlistEntry(CollaborationWhitelistEntry):
    """Represents a allowlisted email domain for enterprise collaboration."""

    _item_type = 'collaboration_whitelist_entry'

    def get_url(self, *args: Any) -> str:
        """
        Gets the collaboration allowlist entries endpoint URL.

        :return:
            The collaboration allowlist entries endpoint URL.
        """
        return self._session.get_url('collaboration_whitelist_entries', self._object_id, *args)
