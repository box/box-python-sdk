# coding: utf-8
from __future__ import unicode_literals, absolute_import
from boxsdk.util.deprecation_decorator import deprecated
from .base_object import BaseObject

class CollaborationWhitelistExemptTarget(BaseObject):
    """Represents a user who is exempted from the collaboration whitelist."""

    _item_type = 'collaboration_whitelist_exempt_target'
