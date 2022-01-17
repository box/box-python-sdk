# coding: utf-8
from typing import Optional, Any

from boxsdk.object.base_object import BaseObject
from boxsdk.util.text_enum import TextEnum
from ..util.api_call_decorator import api_call


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

    @api_call
    def update_info(
            self,
            *,
            role: Optional[CollaborationRole] = None,
            status: Optional[CollaborationStatus] = None,
            **kwargs: Any
    ) -> 'BaseObject':
        """Edit an existing collaboration on Box

        :param role:
            The new role for this collaboration or None to leave unchanged
        :param status:
            The new status for this collaboration or None to leave unchanged. A pending collaboration can be set to
            accepted or rejected if permissions allow it.
        :returns:
            Whether or not the edit was successful.
        :raises:
            :class:`BoxAPIException` if current user doesn't have permissions to edit the collaboration.
        """
        # pylint:disable=arguments-differ
        data = {}
        if role:
            data['role'] = role
        if status:
            data['status'] = status
        if role == CollaborationRole.OWNER:
            return super().update_info(data=data, expect_json_response=False, **kwargs)

        return super().update_info(data=data, **kwargs)

    @api_call
    def accept(self) -> 'BaseObject':
        """Accepts a pending collaboration"""
        return self.update_info(status=CollaborationStatus.ACCEPTED)

    @api_call
    def reject(self) -> 'BaseObject':
        """Rejects a pending collaboration"""
        return self.update_info(status=CollaborationStatus.REJECTED)
