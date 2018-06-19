# coding: utf-8

from __future__ import unicode_literals, absolute_import

from .base_endpoint import BaseEndpoint
from .base_api_json_object import BaseAPIJSONObject


class CollaborationWhitelistExemptTarget(BaseEndpoint, BaseAPIJSONObject):
    """Represents a user who is exempted from the collaboration whitelist."""

    _item_type = 'collaboration_whitelist_exempt_target'
