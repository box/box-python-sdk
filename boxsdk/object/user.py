# coding: utf-8

from __future__ import unicode_literals

import json
from ..config import API
from .base_object import BaseObject


class User(BaseObject):
    """Represents a Box user."""

    _item_type = 'user'

    def add_email_alias(self, email):
        """
        Adds a new email alias to th given user's account.

        :param email:
            The email alias to add to the uer.
        :type email:
            `unicode`
        """
        url = '{0}/users/{1}/email_aliases'.format(API.BASE_API_URL, self.object_id)
        body = {
            'email': email
        }
        response = self._session.post(url, data=json.dumps(body)).json()
        return Translator().translate(response['type'])(
            self._session,
            response['id'],
            response,
        )



