# coding: utf-8

from __future__ import unicode_literals, absolute_import

from .base_endpoint import BaseEndpoint
from .base_api_json_object import BaseAPIJSONObject


class CollaborationWhitelistEntry(BaseEndpoint, BaseAPIJSONObject):
    """Represents a whitelisted email domain for enterprise collaboration."""

    _item_type = 'collaboration_whitelist_entry'
