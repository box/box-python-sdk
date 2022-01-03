# coding: utf-8
import json
from typing import Any, Union, TYPE_CHECKING, Optional, Iterable

from .base_object import BaseObject
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection
from ..util.api_call_decorator import api_call

if TYPE_CHECKING:
    from boxsdk.object.user import User
    from boxsdk.object.folder import Folder
    from boxsdk.object.file import File
    from boxsdk.object.file_version import FileVersion
    from boxsdk.object.legal_hold_policy_assignment import LegalHoldPolicyAssignment
    from boxsdk.pagination.box_object_collection import BoxObjectCollection


class LegalHoldPolicy(BaseObject):
    """Represents a Box legal_hold_policy"""

    _item_type = 'legal_hold_policy'

    def get_url(self, *args: Any) -> str:
        return self._session.get_url('legal_hold_policies', self._object_id, *args)

    @api_call
    def assign(self, assignee: Union['FileVersion', 'File', 'Folder', 'User']) -> 'LegalHoldPolicyAssignment':
        """Assign legal hold policy

        :param assignee:
            The `file_version`, `file`, `folder`, or `user` to assign the legal hold policy to.
        :returns:
            A legal hold policy assignment object
        """
        url = self._session.get_url('legal_hold_policy_assignments')
        body = {
            'policy_id': self.object_id,
            'assign_to': {
                'type': assignee.object_type,
                'id': assignee.object_id
            }
        }
        response = self._session.post(url, data=json.dumps(body)).json()
        return self.translator.translate(
            self._session,
            response,
        )

    @api_call
    def get_assignments(
            self,
            assign_to_type: Optional[str] = None,
            assign_to_id: Optional[str] = None,
            limit: Optional[int] = None,
            marker: Optional[str] = None,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Get the entries in the legal hold policy assignment using limit-offset paging.

        :param assign_to_type:
            Filter assignments of this type only. Can be `file_version`, `file`, `folder`, or `user`
        :param assign_to_id:
            Filter assignments to this ID only
        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :param marker:
            The paging marker to start paging from
        :param fields:
            List of fields to request
        :returns:
            An iterator of the entries in the legal hold policy assignment
        """
        additional_params = {
            'policy_id': self.object_id,
        }
        if assign_to_type is not None:
            additional_params['assign_to_type'] = assign_to_type
        if assign_to_id is not None:
            additional_params['assign_to_id'] = assign_to_id
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self._session.get_url('legal_hold_policy_assignments'),
            additional_params=additional_params,
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )

    @api_call
    def get_file_version_legal_holds(
            self,
            limit: Optional[int] = None,
            marker: Optional[str] = None,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Get legal holds for a file version.

        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :param marker:
            The paging marker to start paging from
        :param fields:
            List of fields to request
        :returns:
            An iterator of the entries in the file version legal holds
        """
        additional_params = {
            'policy_id': self.object_id,
        }
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self._session.get_url('file_version_legal_holds'),
            additional_params=additional_params,
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )
