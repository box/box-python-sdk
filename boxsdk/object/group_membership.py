# coding: utf-8

from .base_object import BaseObject


class GroupMembership(BaseObject):
    """Represents a Box group_membership, which relates a user & group under a specific role."""

    _item_type = 'group_membership'
