# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from .base_object import BaseObject
from .group_membership import GroupMembership


class User(BaseObject):
    """Represents a Box user."""

    _item_type = 'user'

    def groups(self, starting_index=0, limit=100, include_page_info=False):
        """
        A generator over all of the Groups that this User is a member of.

        :param starting_index:
            The index at which to begin.
        :type starting_index:
            `int`
        :param limit:
            The maximum number of items to return in a page.
        :type limit:
            `int`
        :returns:
            A generator of GroupMembership instances. Or, if include_page_info
            is True, it is a generator of 3-tuples, where each tuple is
                1) GroupMembership instance
                2) Number of GroupMemberships returned by the last paged API call
                3) Index of *this* GroupMembership instance in the current page.
        :rtype:
            `generator` of :class:`GroupMembership` or, if include_page_info
            is True then `tuple` of (:class:`GroupMembership`, `int`, `int`)
        """
        url = self.get_url("memberships")
        membership_factory = partial(GroupMembership, user=self)

        for group_membership_tuple in self._paging_wrapper(url, starting_index, limit, membership_factory):
            if include_page_info:
                yield group_membership_tuple
            else:
                group_membership, _, _ = group_membership_tuple
                yield group_membership
