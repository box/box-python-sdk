# coding: utf-8
from __future__ import unicode_literals, absolute_import

from .base_object import BaseObject
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection
from ..util.api_call_decorator import api_call


class RetentionPolicyAssignment(BaseObject):
    """Represents a Box retention policy assignment."""
    _item_type = 'retention_policy_assignment'

    @api_call
    def get_files_under_retention(self, limit=None, marker=None):
        """
        Retrieves all files under retention for a retention policy assignment

        :param limit: the limit of retrieved entries per page. Default 100.
        :param marker: the paging marker to start paging from.
        :return: An iterator of the entries with information about all files under retention.
        :rtype: :class:`BoxObjectCollection`
        """
        return MarkerBasedObjectCollection(
            self.session,
            self.get_url('files_under_retention'),
            limit=limit,
            marker=marker
        )

    @api_call
    def get_file_versions_under_retention(self, limit=None, marker=None):
        """
        Retrieves all file versions under retention for a retention policy assignment

        :param limit: the limit of retrieved entries per page. Default 100.
        :param marker: the paging marker to start paging from.
        :return: An iterator of the entries with information about all files uversions nder retention.
        :rtype: :class:`BoxObjectCollection`
        """
        return MarkerBasedObjectCollection(
            self.session,
            self.get_url('file_versions_under_retention'),
            limit=limit,
            marker=marker
        )
