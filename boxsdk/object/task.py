# coding: utf-8

from __future__ import unicode_literals, absolute_import

from .base_object import BaseObject
from ..util.api_call_decorator import api_call


class Task(BaseObject):
    """Represents a Box file task."""

    _item_type = 'task'

    @api_call
    def assignments(self):
        """
        Gets assignments associated with this task.

        :return:
            Task assignments associated with this task.
        :rtype:
            `list` of :class:`TaskAssignment`
        """
        url = self.get_url('assignments')
        box_response = self._session.get(url)
        response = box_response.json()
        return [self.translator.translate('task_assignment')(self._session, item['id'], item) for item in response['entries']]
