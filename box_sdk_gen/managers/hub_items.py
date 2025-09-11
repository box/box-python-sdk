from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from typing import List

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.v2025_r0.hub_item_operation_v2025_r0 import (
    HubItemOperationV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_items_v2025_r0 import HubItemsV2025R0

from box_sdk_gen.schemas.v2025_r0.client_error_v2025_r0 import ClientErrorV2025R0

from box_sdk_gen.parameters.v2025_r0.box_version_header_v2025_r0 import (
    BoxVersionHeaderV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_items_manage_response_v2025_r0 import (
    HubItemsManageResponseV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_items_manage_request_v2025_r0 import (
    HubItemsManageRequestV2025R0,
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


class HubItemsManager:
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

    def get_hub_items_v2025_r0(
        self,
        hub_id: str,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> HubItemsV2025R0:
        """
                Retrieves all items associated with a Box Hub.
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
                    [self.network_session.base_urls.base_url, '/2.0/hub_items']
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, HubItemsV2025R0)

    def manage_hub_items_v2025_r0(
        self,
        hub_id: str,
        *,
        operations: Optional[List[HubItemOperationV2025R0]] = None,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> HubItemsManageResponseV2025R0:
        """
                Adds and/or removes Box Hub items from a Box Hub.
                :param hub_id: The unique identifier that represent a hub.

        The ID for any hub can be determined
        by visiting this hub in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/hubs/123`
        the `hub_id` is `123`.
        Example: "12345"
                :type hub_id: str
                :param operations: List of operations to perform on Box Hub items., defaults to None
                :type operations: Optional[List[HubItemOperationV2025R0]], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2025R0._2025_0
                :type box_version: BoxVersionHeaderV2025R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'operations': operations}
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
                        '/manage_items',
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
        return deserialize(response.data, HubItemsManageResponseV2025R0)
