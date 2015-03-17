# coding: utf-8

from __future__ import unicode_literals

from boxsdk.object.base_object import BaseObject
from boxsdk.util.text_enum import TextEnum


class CollaborationRole(TextEnum):
    """An enum of possible collaboration roles"""
    EDITOR = 'editor'
    VIEWER = 'viewer'

    # Available to enterprise accounts:
    PREVIEWER = 'previewer'
    UPLOADER = 'uploader'
    PREVIEWER_UPLOADER = 'previewer uploader'
    VIEWER_UPLOADER = 'viewer uploader'
    CO_OWNER = 'co-owner'
    OWNER = 'owner'


class CollaborationStatus(TextEnum):
    """An enum of possible statuses of a collaboration"""
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


class Collaboration(BaseObject):
    """An object that represents a collaboration between a folder and an individual or group"""
    _item_type = 'collaboration'

    # pylint:disable=arguments-differ
    def update_info(self, role=None, status=None):
        """Edit an existing collaboration on Box

        :param role:
            The new role for this collaboration or None to leave unchanged
        :type role:
            :class:`CollaborationRole`
        :param status:
            The new status for this collaboration or None to leave unchanged. A pending collaboration can be set to
            accepted or rejected if permissions allow it.
        :type status:
            :class:`CollaborationStatus`
        :returns:
            Whether or not the edit was successful.
        :rtype:
            `bool`
        :raises:
            :class:`BoxAPIException` if current user doesn't have permissions to edit the collaboration.
        """
        data = {}
        if role:
            data['role'] = role
        if status:
            data['status'] = status
        return super(Collaboration, self).update_info(data=data)
