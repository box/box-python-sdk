# coding: utf-8

from __future__ import unicode_literals, absolute_import

import json

from boxsdk.object.base_object import BaseObject
from ..util.api_call_decorator import api_call

class Comment(BaseObject):
    """An object that represents a comment on an item"""
    _item_type = 'comment'

    @api_call
    def reply(self, message):
        """
        Add a reply to the comment.

        :param message:
            The content of the reply comment.
        :type message:
            `unicode`
        """
        url = self.get_type_url()
        message_type = 'tagged_message' if '@[' in message else 'message'
        data = {
            message_type: message,
            'item': {
                'type': 'comment',
                'id': self.object_id
            }
        }
        box_response = self._session.post(url, data=json.dumps(data))
        response = box_response.json()
        return self.__class__(
            session=self._session,
            object_id=response['id'],
            response_object=response,
        )

    @api_call
    def edit(self, message):
        """
        Edit the message of the comment.

        :param message:
            The content of the reply comment.
        :type message:
            `unicode`
        """
        message_type = 'tagged_message' if '@[' in message else 'message'
        data = {
            message_type: message
        }
        return self.update_info(data)
