# coding: utf-8
import json
from typing import Optional, Iterable, TYPE_CHECKING

from .base_endpoint import BaseEndpoint
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection
from ..util.api_call_decorator import api_call
from ..util.text_enum import TextEnum

if TYPE_CHECKING:
    from boxsdk.pagination.box_object_collection import BoxObjectCollection
    from boxsdk.object.collaboration_allowlist_entry import CollaborationAllowlistEntry
    from boxsdk.object.user import User
    from boxsdk.object.collaboration_allowlist_exempt_target import CollaborationAllowlistExemptTarget


class AllowlistDirection(TextEnum):
    """
    Used to determine the direction of the allowlist.
    """
    INBOUND = 'inbound'
    OUTBOUNT = 'outbound'
    BOTH = 'both'


class CollaborationAllowlist(BaseEndpoint):
    """Represents the allowlist of email domains that users in an enterprise may collaborate with."""

    @api_call
    def get_entries(
            self,
            limit: Optional[int] = None,
            marker: Optional[str] = None,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Get the entries in the collaboration allowlist using limit-offset paging.

        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :param marker:
            The paging marker to start paging from.
        :param fields:
            List of fields to request.
        :returns:
            An iterator of the entries in the allowlist.
        """
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self.get_url('collaboration_whitelist_entries'),
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )

    @api_call
    def add_domain(self, domain: str, direction: str) -> 'CollaborationAllowlistEntry':
        """
        Add a new domain to the collaboration allowlist.

        :param domain:
            The email domain to add to the allowlist.
        :param direction:
            The direction in which collaboration should be allowed: 'inbound', 'outbound', or 'both'.
        :returns:
            The created allowlist entry for the domain.
        """
        url = self.get_url('collaboration_whitelist_entries')
        data = {
            'domain': domain,
            'direction': direction
        }
        response = self._session.post(url, data=json.dumps(data)).json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def get_exemptions(
            self,
            limit: Optional[int] = None,
            marker: Optional[str] = None,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Get the list of exempted users who are not subject to the collaboration allowlist rules.

        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :param marker:
            The paging marker to start paging from.
        :param fields:
            List of fields to request.
        :returns:
            An iterator of the exemptions to the allowlist.
        """
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self.get_url('collaboration_whitelist_exempt_targets'),
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )

    @api_call
    def add_exemption(self, user: 'User') -> 'CollaborationAllowlistExemptTarget':
        """
        Exempt a user from the collaboration allowlist.

        :param user:
            The user to exempt from the allowlist.
        :returns:
            The created allowlist exemption.
        """
        url = self.get_url('collaboration_whitelist_exempt_targets')
        data = {
            'user': {
                'id': user.object_id  # pylint:disable=protected-access
            }
        }
        response = self._session.post(url, data=json.dumps(data)).json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )
