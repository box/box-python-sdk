from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.v2025_r0.hub_collaborations_v2025_r0 import (
    HubCollaborationsV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.client_error_v2025_r0 import ClientErrorV2025R0

from box_sdk_gen.parameters.v2025_r0.box_version_header_v2025_r0 import (
    BoxVersionHeaderV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_collaboration_v2025_r0 import (
    HubCollaborationV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_collaboration_create_request_v2025_r0 import (
    HubCollaborationCreateRequestV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_collaboration_update_request_v2025_r0 import (
    HubCollaborationUpdateRequestV2025R0,
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


class CreateHubCollaborationV2025R0HubTypeField(str, Enum):
    HUBS = 'hubs'


class CreateHubCollaborationV2025R0Hub(BaseObject):
    _discriminator = 'type', {'hubs'}

    def __init__(
        self,
        id: str,
        *,
        type: CreateHubCollaborationV2025R0HubTypeField = CreateHubCollaborationV2025R0HubTypeField.HUBS,
        **kwargs
    ):
        """
        :param id: ID of the object.
        :type id: str
        :param type: The value will always be `hubs`., defaults to CreateHubCollaborationV2025R0HubTypeField.HUBS
        :type type: CreateHubCollaborationV2025R0HubTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class CreateHubCollaborationV2025R0AccessibleBy(BaseObject):
    def __init__(
        self,
        type: str,
        *,
        id: Optional[str] = None,
        login: Optional[str] = None,
        **kwargs
    ):
        """
                :param type: The type of collaborator to invite.
        Possible values are `user` or `group`.
                :type type: str
                :param id: The ID of the user or group.

        Alternatively, use `login` to specify a user by email
        address., defaults to None
                :type id: Optional[str], optional
                :param login: The email address of the user who gets access to the item.

        Alternatively, use `id` to specify a user by user ID., defaults to None
                :type login: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id
        self.login = login


class HubCollaborationsManager:
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

    def get_hub_collaborations_v2025_r0(
        self,
        hub_id: str,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> HubCollaborationsV2025R0:
        """
                Retrieves all collaborations for a Box Hub.
                :param hub_id: The unique identifier that represent a hub.

        The ID for any hub can be determined
        by visiting this hub in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/hubs/123`
        the `hub_id` is `123`.
                :type hub_id: str
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2025R0._2025_0
                :type box_version: BoxVersionHeaderV2025R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'hub_id': to_string(hub_id),
                'marker': to_string(marker),
                'limit': to_string(limit),
            }
        )
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/hub_collaborations']
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, HubCollaborationsV2025R0)

    def create_hub_collaboration_v2025_r0(
        self,
        hub: CreateHubCollaborationV2025R0Hub,
        accessible_by: CreateHubCollaborationV2025R0AccessibleBy,
        role: str,
        *,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> HubCollaborationV2025R0:
        """
                Adds a collaboration for a single user or a single group to a Box Hub.

                Collaborations can be created using email address, user IDs, or group IDs.

                :param hub: Box Hubs reference.
                :type hub: CreateHubCollaborationV2025R0Hub
                :param accessible_by: The user or group who gets access to the item.
                :type accessible_by: CreateHubCollaborationV2025R0AccessibleBy
                :param role: The level of access granted to a Box Hub.
        Possible values are `editor`, `viewer`, and `co-owner`.
                :type role: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2025R0._2025_0
                :type box_version: BoxVersionHeaderV2025R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'hub': hub, 'accessible_by': accessible_by, 'role': role}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/hub_collaborations']
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
        return deserialize(response.data, HubCollaborationV2025R0)

    def get_hub_collaboration_by_id_v2025_r0(
        self,
        hub_collaboration_id: str,
        *,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> HubCollaborationV2025R0:
        """
                Retrieves details for a Box Hub collaboration by collaboration ID.
                :param hub_collaboration_id: The ID of the hub collaboration.
        Example: "1234"
                :type hub_collaboration_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2025R0._2025_0
                :type box_version: BoxVersionHeaderV2025R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/hub_collaborations/',
                        to_string(hub_collaboration_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, HubCollaborationV2025R0)

    def update_hub_collaboration_by_id_v2025_r0(
        self,
        hub_collaboration_id: str,
        *,
        role: Optional[str] = None,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> HubCollaborationV2025R0:
        """
                Updates a Box Hub collaboration.

                Can be used to change the Box Hub role.

                :param hub_collaboration_id: The ID of the hub collaboration.
        Example: "1234"
                :type hub_collaboration_id: str
                :param role: The level of access granted to a Box Hub.
        Possible values are `editor`, `viewer`, and `co-owner`., defaults to None
                :type role: Optional[str], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2025R0._2025_0
                :type box_version: BoxVersionHeaderV2025R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'role': role}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/hub_collaborations/',
                        to_string(hub_collaboration_id),
                    ]
                ),
                method='PUT',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, HubCollaborationV2025R0)

    def delete_hub_collaboration_by_id_v2025_r0(
        self,
        hub_collaboration_id: str,
        *,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Deletes a single Box Hub collaboration.
                :param hub_collaboration_id: The ID of the hub collaboration.
        Example: "1234"
                :type hub_collaboration_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2025R0._2025_0
                :type box_version: BoxVersionHeaderV2025R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/hub_collaborations/',
                        to_string(hub_collaboration_id),
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
