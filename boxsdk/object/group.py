# coding: utf-8

from __future__ import unicode_literals
from functools import partial
import json

from .base_object import BaseObject
from boxsdk.config import API
from boxsdk.object.group_membership import GroupMembership


class Group(BaseObject):
    """Represents a Box group."""

    _item_type = 'group'

    def membership(self, starting_index=0, limit=100, include_page_info=False):
        """
        A generator over all the members of this Group. The paging in the API is transparently implemented
        inside the generator. By adjusting the page_size, the caller can control the chattiness of the API. Caller
        can also implement their owning paging and/or control exactly when an API is called by
        using the 'include_page_info' param as follows:

            for group, page_size, index in group.membership(..., include_page_info=True):
                # when index + 1 == page_size, the next iteration of this loop will
                # trigger an API call, unless we've reached the end of *all* the data.
                pass

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
        url = self.get_url('memberships')

        membership_factory = partial(GroupMembership, group=self)
        for group_membership_tuple in self._paging_wrapper(url, starting_index, limit, membership_factory):
            if include_page_info:
                yield group_membership_tuple
            else:
                group_membership, _, _ = group_membership_tuple
                yield group_membership

    def add_member(self, user, role):
        """
        Add the given user to this group under the given role

        :param user:
            The User to add to the group.
        :type user:
            :class:`User`
        :param role:
            The role for the user. TODO: determine valid options and create an Enum.
        :type role:
            `unicode`
        :returns:
            The new GroupMembership instance.
        :rtype:
            :class:`GroupMembership`
        """
        url = '{0}/group_memberships'.format(API.BASE_API_URL)
        body_attributes = {
            'user': {'id': user.object_id},
            'group': {'id': self.object_id},
            'role': role,
        }
        box_response = self._session.post(url, data=json.dumps(body_attributes))
        response = box_response.json()

        return GroupMembership(self._session, response['id'], response, user=user, group=self)
