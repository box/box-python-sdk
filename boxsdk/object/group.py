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

    def membership(self, starting_index=0, limit=100):
        """
        A generator over all the members of this Group. The paging in the API is transparently implemented
        inside the generator. By adjusting the page_size, the caller can control the chattiness of the API. Caller
        can also implement their owning paging and/or control exactly when an API is called:

            def get_slice(group, start, limit):
                return list(itertools.islice(group.membership(..., start, limit, ...), limit))

            first_ten = get_slice(some_group, 0, 10)
            second_ten = get_slice(some_group, 10, 10)
            third_ten = get_slice(some_group, 20, 10)

        caveat - any hidden items (see the Box Developer API for more details) will render the above
        inaccurate. Hidden results will lead the above get_slice() code to trigger API calls at non-expected places.

        :param starting_index:
            The index at which to begin.
        :type starting_index:
            `int`
        :param limit:
            The maximum number of items to return in a page.
        :type limit:
            `int`
        :returns:
            A generator of GroupMembership instances.
        :rtype:
            `generator` of :class:`GroupMembership`
        """
        url = self.get_url('memberships')

        membership_factory = partial(GroupMembership, group=self)
        for group_membership in self._paging_wrapper(url, starting_index, limit, membership_factory):
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
