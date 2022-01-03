# coding: utf-8
import json
from typing import TYPE_CHECKING

from .base_object import BaseObject
from ..util.api_call_decorator import api_call

if TYPE_CHECKING:
    from boxsdk.object.invite import Invite


class Enterprise(BaseObject):

    """Represents a single enterprise."""
    _item_type = 'enterprise'

    @api_call
    def invite_user(self, user_email: str) -> 'Invite':
        """
        Invites an existing user to an Enterprise. The user must already have a Box account.

        :param user_email:
            The login email address of the user that will receive the invitation.
        :returns:
            The invitation record for the user
        """
        url = self._session.get_url('invites')
        body = {
            'enterprise': {
                'id': self.object_id,
            },
            'actionable_by': {
                'login': user_email,
            },
        }
        response = self._session.post(url, data=json.dumps(body)).json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )
