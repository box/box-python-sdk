# coding: utf-8
from __future__ import unicode_literals

import json

from boxsdk.object.base_object import BaseObject
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection
from ..util.api_call_decorator import api_call


class Task(BaseObject):
    """Represents a Box task."""
    _item_type = 'task'

    @api_call
    def assign(self, assignee):
        """
        Assign a task to a single user on a single file.

        :param assignee:
            The :class:`User` to assign the task to.
        :type assignee:
            :class:`User`
        :returns:
            A task assignment object.
        :rtype:
            :class:`TaskAssignment`
        """
        url = self._session.get_url('task_assignments')
        body = {
            'task': {
                'type': 'task',
                'id': self.object_id,
            },
            'assign_to': {
                'id': assignee.object_id,
            },
        }
        response = self._session.post(url, data=json.dumps(body)).json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def assign_with_login(self, assignee_login):
        """
        Used to assign a task to a single user with the login email address of the assignee.

        :param assign_to_login:
            The login of the user to assign the task to.
        :type assign_to_login:
            `unicode` or None
        :returns:
            A task assignment object.
        :rtype:
            :class:`TaskAssignment`
        """
        url = self._session.get_url('task_assignments')
        body = {
            'task': {
                'type': 'task',
                'id': self.object_id,
            },
            'assign_to': {
                'login': assignee_login,
            },
        }
        response = self._session.post(url, data=json.dumps(body)).json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def get_assignments(self, fields=None):
        """
        Get the entries in the file task assignment.

        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries in the file task assignment.
        :rtype:
            :class:`BoxObjectCollection`
        """
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self.get_url('assignments'),
            limit=None,
            marker=None,
            fields=fields,
            return_full_pages=False,
        )
