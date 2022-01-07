# coding: utf-8

import json

from boxsdk.object.base_object import BaseObject
from ..util.api_call_decorator import api_call


class Comment(BaseObject):
    """An object that represents a comment on an item"""
    _item_type = 'comment'

    @staticmethod
    def construct_params_from_message(message: str) -> dict:
        message_type = 'tagged_message' if '@[' in message else 'message'
        return {
            message_type: message
        }

    @api_call
    def reply(self, message: str) -> 'Comment':
        """
        Add a reply to the comment.

        :param message:
            The content of the reply comment.
        """
        url = self.get_type_url()
        data = self.construct_params_from_message(message)
        data['item'] = {
            'type': 'comment',
            'id': self.object_id
        }
        box_response = self._session.post(url, data=json.dumps(data))
        response = box_response.json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def edit(self, message: str) -> 'Comment':
        """
        Edit the message of the comment.

        :param message:
            The content of the reply comment.
        """
        data = self.construct_params_from_message(message)
        return self.update_info(data=data)
