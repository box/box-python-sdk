# coding: utf-8
import json
from typing import Any, Union, TYPE_CHECKING, Iterable, Optional
from .base_object import BaseObject
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection
from ..util.api_call_decorator import api_call

if TYPE_CHECKING:
    from boxsdk.object.metadata_template import MetadataTemplate
    from boxsdk.object.enterprise import Enterprise
    from boxsdk.object.folder import Folder
    from boxsdk.object.retention_policy_assignment import RetentionPolicyAssignment
    from boxsdk.pagination.box_object_collection import BoxObjectCollection


class RetentionPolicy(BaseObject):
    """Represents a Box retention policy."""
    _item_type = 'retention_policy'

    def get_url(self, *args: Any) -> str:
        """
        Returns the url for this retention policy.
        """
        return self._session.get_url('retention_policies', self._object_id, *args)

    @api_call
    def assign(
            self,
            assignee: Union['Folder', 'Enterprise', 'MetadataTemplate'],
            fields: Iterable[str] = None
    ) -> 'RetentionPolicyAssignment':
        """Assign a retention policy to a Box item

        :param assignee:
            The item to assign the retention policy on.
        :param fields:
            List of fields to request.
        :returns:
            A :class:`RetentionPolicyAssignment` object.
        """
        url = self._session.get_url('retention_policy_assignments')
        body = {
            'policy_id': self.object_id,
            'assign_to': {
                'type': assignee.object_type,
                'id': assignee.object_id,
            }
        }
        params = {}
        if fields is not None:
            params['fields'] = ','.join(fields)
        response = self._session.post(url, data=json.dumps(body), params=params).json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def assignments(
            self,
            assignment_type: Optional[str] = None,
            limit: Optional[int] = None,
            marker: Optional[str] = None,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """Get the assignments for the retention policy.

        :param assignment_type:
            The type of retention policy assignment to retrieve. Can be set to 'folder', 'enterprise', or 'metadata_template'.
        :param limit:
            The maximum number of items to return.
        :param marker:
            The position marker at which to begin the response.
        :param fields:
            List of fields to request.
        :returns:
            An iterable of assignments in the retention policy.
        """
        additional_params = {}
        if assignment_type is not None:
            additional_params['assignment_type'] = assignment_type
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self.get_url('assignments'),
            additional_params=additional_params,
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )
