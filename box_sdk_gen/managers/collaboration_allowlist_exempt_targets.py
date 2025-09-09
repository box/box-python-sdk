from box_sdk_gen.internal.base_object import BaseObject

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.collaboration_allowlist_exempt_targets import (
    CollaborationAllowlistExemptTargets,
)

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.collaboration_allowlist_exempt_target import (
    CollaborationAllowlistExemptTarget,
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


class CreateCollaborationWhitelistExemptTargetUser(BaseObject):
    def __init__(self, id: str, **kwargs):
        """
        :param id: The ID of the user to exempt.
        :type id: str
        """
        super().__init__(**kwargs)
        self.id = id


class CollaborationAllowlistExemptTargetsManager:
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

    def get_collaboration_whitelist_exempt_targets(
        self,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> CollaborationAllowlistExemptTargets:
        """
                Returns a list of users who have been exempt from the collaboration

                domain restrictions.

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
                        '/2.0/collaboration_whitelist_exempt_targets',
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
        return deserialize(response.data, CollaborationAllowlistExemptTargets)

    def create_collaboration_whitelist_exempt_target(
        self,
        user: CreateCollaborationWhitelistExemptTargetUser,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> CollaborationAllowlistExemptTarget:
        """
        Exempts a user from the restrictions set out by the allowed list of domains

        for collaborations.

        :param user: The user to exempt.
        :type user: CreateCollaborationWhitelistExemptTargetUser
        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'user': user}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/collaboration_whitelist_exempt_targets',
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
        return deserialize(response.data, CollaborationAllowlistExemptTarget)

    def get_collaboration_whitelist_exempt_target_by_id(
        self,
        collaboration_whitelist_exempt_target_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> CollaborationAllowlistExemptTarget:
        """
                Returns a users who has been exempt from the collaboration

                domain restrictions.

                :param collaboration_whitelist_exempt_target_id: The ID of the exemption to the list.
        Example: "984923"
                :type collaboration_whitelist_exempt_target_id: str
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
                        '/2.0/collaboration_whitelist_exempt_targets/',
                        to_string(collaboration_whitelist_exempt_target_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, CollaborationAllowlistExemptTarget)

    def delete_collaboration_whitelist_exempt_target_by_id(
        self,
        collaboration_whitelist_exempt_target_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Removes a user's exemption from the restrictions set out by the allowed list

                of domains for collaborations.

                :param collaboration_whitelist_exempt_target_id: The ID of the exemption to the list.
        Example: "984923"
                :type collaboration_whitelist_exempt_target_id: str
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
                        '/2.0/collaboration_whitelist_exempt_targets/',
                        to_string(collaboration_whitelist_exempt_target_id),
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
