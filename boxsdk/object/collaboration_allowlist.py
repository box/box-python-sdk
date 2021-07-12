# coding: utf-8
from __future__ import unicode_literals, absolute_import

import json

from .base_endpoint import BaseEndpoint
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection
from ..util.api_call_decorator import api_call
from ..util.text_enum import TextEnum


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
    def get_entries(self, limit=None, marker=None, fields=None):
        """
        Get the entries in the collaboration allowlist using limit-offset paging.

        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param marker:
            The paging marker to start paging from.
        :type marker:
            `unicode` or None
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries in the allowlist.
        :rtype:
            :class:`BoxObjectCollection`
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
    def add_domain(self, domain, direction):
        """
        Add a new domain to the collaboration allowlist.

        :param domain:
            The email domain to add to the allowlist.
        :type domain:
            `unicode`
        :param direction:
            The direction in which collaboration should be allowed: 'inbound', 'outbound', or 'both'.
        :type direction:
            `unicode`
        :returns:
            The created allowlist entry for the domain.
        :rtype:
            :class:`CollaborationAllowlistEntry`
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
    def get_exemptions(self, limit=None, marker=None, fields=None):
        """
        Get the list of exempted users who are not subject to the collaboration allowlist rules.

        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param marker:
            The paging marker to start paging from.
        :type marker:
            `unicode` or None
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the exemptions to the allowlist.
        :rtype:
            :class:`BoxObjectCollection`
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
    def add_exemption(self, user):
        """
        Exempt a user from the collaboration allowlist.

        :param user:
            The user to exempt from the allowlist.
        :type user:
            :class:`User`
        :returns:
            The created allowlist exemption.
        :rtype:
            :class:`CollaborationAllowlistExemptTarget`
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
