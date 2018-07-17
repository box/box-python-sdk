# coding:utf-8

from __future__ import unicode_literals, absolute_import

from .base_object import BaseObject

class StoragePolicyAssignment(BaseObject):
    """Represents the storage policy assignment"""

    def get_url(self, *args):
        return self._session.get_url('storage_policy_assignments', self._object_id, *args)

    _item_type = 'storage_policy_assignment'
