from enum import Enum

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.v2025_r0.hubs_v2025_r0 import HubsV2025R0

from box_sdk_gen.schemas.v2025_r0.client_error_v2025_r0 import ClientErrorV2025R0

from box_sdk_gen.parameters.v2025_r0.box_version_header_v2025_r0 import (
    BoxVersionHeaderV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_v2025_r0 import HubV2025R0

from box_sdk_gen.schemas.v2025_r0.hub_create_request_v2025_r0 import (
    HubCreateRequestV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_update_request_v2025_r0 import (
    HubUpdateRequestV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_copy_request_v2025_r0 import HubCopyRequestV2025R0

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


class GetHubsV2025R0Direction(str, Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class GetEnterpriseHubsV2025R0Direction(str, Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class HubsManager:
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

    def get_hubs_v2025_r0(
        self,
        *,
        query: Optional[str] = None,
        scope: Optional[str] = None,
        sort: Optional[str] = None,
        direction: Optional[GetHubsV2025R0Direction] = None,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> HubsV2025R0:
        """
                Retrieves all Box Hubs for requesting user.
                :param query: The query string to search for Box Hubs., defaults to None
                :type query: Optional[str], optional
                :param scope: The scope of the Box Hubs to retrieve. Possible values include `editable`,
        `view_only`, and `all`. Default is `all`., defaults to None
                :type scope: Optional[str], optional
                :param sort: The field to sort results by.
        Possible values include `name`, `updated_at`,
        `last_accessed_at`, `view_count`, and `relevance`.
        Default is `relevance`., defaults to None
                :type sort: Optional[str], optional
                :param direction: The direction to sort results in. This can be either in alphabetical ascending
        (`ASC`) or descending (`DESC`) order., defaults to None
                :type direction: Optional[GetHubsV2025R0Direction], optional
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination., defaults to None
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
                'query': to_string(query),
                'scope': to_string(scope),
                'sort': to_string(sort),
                'direction': to_string(direction),
                'marker': to_string(marker),
                'limit': to_string(limit),
            }
        )
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join([self.network_session.base_urls.base_url, '/2.0/hubs']),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, HubsV2025R0)

    def create_hub_v2025_r0(
        self,
        title: str,
        *,
        description: Optional[str] = None,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> HubV2025R0:
        """
        Creates a new Box Hub.
        :param title: Title of the Box Hub. It cannot be empty and should be less than 50 characters.
        :type title: str
        :param description: Description of the Box Hub., defaults to None
        :type description: Optional[str], optional
        :param box_version: Version header., defaults to BoxVersionHeaderV2025R0._2025_0
        :type box_version: BoxVersionHeaderV2025R0, optional
        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'title': title, 'description': description}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join([self.network_session.base_urls.base_url, '/2.0/hubs']),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, HubV2025R0)

    def get_enterprise_hubs_v2025_r0(
        self,
        *,
        query: Optional[str] = None,
        sort: Optional[str] = None,
        direction: Optional[GetEnterpriseHubsV2025R0Direction] = None,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> HubsV2025R0:
        """
                Retrieves all Box Hubs for a given enterprise.

                Admins or Hub Co-admins of an enterprise


                with GCM scope can make this call.

                :param query: The query string to search for Box Hubs., defaults to None
                :type query: Optional[str], optional
                :param sort: The field to sort results by.
        Possible values include `name`, `updated_at`,
        `last_accessed_at`, `view_count`, and `relevance`.
        Default is `relevance`., defaults to None
                :type sort: Optional[str], optional
                :param direction: The direction to sort results in. This can be either in alphabetical ascending
        (`ASC`) or descending (`DESC`) order., defaults to None
                :type direction: Optional[GetEnterpriseHubsV2025R0Direction], optional
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination., defaults to None
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
                'query': to_string(query),
                'sort': to_string(sort),
                'direction': to_string(direction),
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
                    [self.network_session.base_urls.base_url, '/2.0/enterprise_hubs']
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, HubsV2025R0)

    def get_hub_by_id_v2025_r0(
        self,
        hub_id: str,
        *,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> HubV2025R0:
        """
                Retrieves details for a Box Hub by its ID.
                :param hub_id: The unique identifier that represent a hub.

        The ID for any hub can be determined
        by visiting this hub in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/hubs/123`
        the `hub_id` is `123`.
        Example: "12345"
                :type hub_id: str
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
                        '/2.0/hubs/',
                        to_string(hub_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, HubV2025R0)

    def update_hub_by_id_v2025_r0(
        self,
        hub_id: str,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        is_ai_enabled: Optional[bool] = None,
        is_collaboration_restricted_to_enterprise: Optional[bool] = None,
        can_non_owners_invite: Optional[bool] = None,
        can_shared_link_be_created: Optional[bool] = None,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> HubV2025R0:
        """
                Updates a Box Hub. Can be used to change title, description, or Box Hub settings.
                :param hub_id: The unique identifier that represent a hub.

        The ID for any hub can be determined
        by visiting this hub in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/hubs/123`
        the `hub_id` is `123`.
        Example: "12345"
                :type hub_id: str
                :param title: Title of the Box Hub. It cannot be empty and should be less than 50 characters., defaults to None
                :type title: Optional[str], optional
                :param description: Description of the Box Hub., defaults to None
                :type description: Optional[str], optional
                :param is_ai_enabled: Indicates if AI features are enabled for the Box Hub., defaults to None
                :type is_ai_enabled: Optional[bool], optional
                :param is_collaboration_restricted_to_enterprise: Indicates if collaboration is restricted to the enterprise., defaults to None
                :type is_collaboration_restricted_to_enterprise: Optional[bool], optional
                :param can_non_owners_invite: Indicates if non-owners can invite others to the Box Hub., defaults to None
                :type can_non_owners_invite: Optional[bool], optional
                :param can_shared_link_be_created: Indicates if a shared link can be created for the Box Hub., defaults to None
                :type can_shared_link_be_created: Optional[bool], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2025R0._2025_0
                :type box_version: BoxVersionHeaderV2025R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'title': title,
            'description': description,
            'is_ai_enabled': is_ai_enabled,
            'is_collaboration_restricted_to_enterprise': (
                is_collaboration_restricted_to_enterprise
            ),
            'can_non_owners_invite': can_non_owners_invite,
            'can_shared_link_be_created': can_shared_link_be_created,
        }
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/hubs/',
                        to_string(hub_id),
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
        return deserialize(response.data, HubV2025R0)

    def delete_hub_by_id_v2025_r0(
        self,
        hub_id: str,
        *,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Deletes a single Box Hub.
                :param hub_id: The unique identifier that represent a hub.

        The ID for any hub can be determined
        by visiting this hub in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/hubs/123`
        the `hub_id` is `123`.
        Example: "12345"
                :type hub_id: str
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
                        '/2.0/hubs/',
                        to_string(hub_id),
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

    def copy_hub_v2025_r0(
        self,
        hub_id: str,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> HubV2025R0:
        """
                Creates a copy of a Box Hub.

                The original Box Hub will not be modified.

                :param hub_id: The unique identifier that represent a hub.

        The ID for any hub can be determined
        by visiting this hub in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/hubs/123`
        the `hub_id` is `123`.
        Example: "12345"
                :type hub_id: str
                :param title: Title of the Box Hub. It cannot be empty and should be less than 50 characters., defaults to None
                :type title: Optional[str], optional
                :param description: Description of the Box Hub., defaults to None
                :type description: Optional[str], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2025R0._2025_0
                :type box_version: BoxVersionHeaderV2025R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'title': title, 'description': description}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/hubs/',
                        to_string(hub_id),
                        '/copy',
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
        return deserialize(response.data, HubV2025R0)
