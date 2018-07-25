# coding: utf-8

from __future__ import unicode_literals

import json
from ..config import API
from .base_object import BaseObject
from ..util.translator import Translator
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection


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


    def email_aliases(self, fields=None):
        """
        :param fields:
            List of fields to request
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries email alias
        """
        return MarkerBasedObjectCollection(
            session=self._session,
            url='{0}/users/{1}/email_aliases'.format(API.BASE_API_URL, self.object_id),
            marker=None,
            fields=fields,
            return_full_pages=False
        )


    def move_owned_items(self, user_id, notify=None, fields=None):
        """
        Move all of the items owned by a user into a new folder in another user’s account.

        :param user_id:
            The id of the user to transfer content to.
        :type version_id:
            `unicode`
        :param notify:
            Whether the destination user should receive email notification of the transfer.
        :type notify:
            `boolean`
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        """
        url = '{0}/users/{1}/folders/{2}'.format(API.BASE_API_URL, user_id, '0')
        body = {
            'owned_by': {
                'id': self.object_id
            }
        }
        response = self._session.put(url, data=json.dumps(body)).json()
        return Translator().translate(response['type'])(
            self._session,
            response['id'],
            response,
        )



