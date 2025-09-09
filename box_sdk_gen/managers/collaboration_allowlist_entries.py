from enum import Enum

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.collaboration_allowlist_entries import (
    CollaborationAllowlistEntries,
)

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.collaboration_allowlist_entry import (
    CollaborationAllowlistEntry,
)

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import prepare_params

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.serialization.json import sd_to_json

from box_sdk_gen.serialization.json import SerializedData


class CreateCollaborationWhitelistEntryDirection(str, Enum):
    INBOUND = 'inbound'
    OUTBOUND = 'outbound'
    BOTH = 'both'


class CollaborationAllowlistEntriesManager:
    def __init__(
        self,
        *,
        auth: Optional[Authentication] = None,
        network_session: NetworkSession = None
    ):
        if network_session is None:
            network_session = NetworkSession()
        self.auth = auth
        self.network_session = network_session

    def get_collaboration_whitelist_entries(
        self,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> CollaborationAllowlistEntries:
        """
                Returns the list domains that have been deemed safe to create collaborations

                for within the current enterprise.

                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {'marker': to_string(marker), 'limit': to_string(limit)}
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/collaboration_whitelist_entries',
                    ]
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, CollaborationAllowlistEntries)

    def create_collaboration_whitelist_entry(
        self,
        domain: str,
        direction: CreateCollaborationWhitelistEntryDirection,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> CollaborationAllowlistEntry:
        """
        Creates a new entry in the list of allowed domains to allow

        collaboration for.

        :param domain: The domain to add to the list of allowed domains.
        :type domain: str
        :param direction: The direction in which to allow collaborations.
        :type direction: CreateCollaborationWhitelistEntryDirection
        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'domain': domain, 'direction': direction}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/collaboration_whitelist_entries',
                    ]
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, CollaborationAllowlistEntry)

    def get_collaboration_whitelist_entry_by_id(
        self,
        collaboration_whitelist_entry_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> CollaborationAllowlistEntry:
        """
                Returns a domain that has been deemed safe to create collaborations

                for within the current enterprise.

                :param collaboration_whitelist_entry_id: The ID of the entry in the list.
        Example: "213123"
                :type collaboration_whitelist_entry_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/collaboration_whitelist_entries/',
                        to_string(collaboration_whitelist_entry_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, CollaborationAllowlistEntry)

    def delete_collaboration_whitelist_entry_by_id(
        self,
        collaboration_whitelist_entry_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Removes a domain from the list of domains that have been deemed safe to create

                collaborations for within the current enterprise.

                :param collaboration_whitelist_entry_id: The ID of the entry in the list.
        Example: "213123"
                :type collaboration_whitelist_entry_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/collaboration_whitelist_entries/',
                        to_string(collaboration_whitelist_entry_id),
                    ]
                ),
                method='DELETE',
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None
