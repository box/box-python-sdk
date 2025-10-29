from typing import Optional

from typing import List

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_v2025_r0 import (
    EnterpriseConfigurationV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.client_error_v2025_r0 import ClientErrorV2025R0

from box_sdk_gen.parameters.v2025_r0.box_version_header_v2025_r0 import (
    BoxVersionHeaderV2025R0,
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


class EnterpriseConfigurationsManager:
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

    def get_enterprise_configuration_by_id_v2025_r0(
        self,
        enterprise_id: str,
        categories: List[str],
        *,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> EnterpriseConfigurationV2025R0:
        """
                Retrieves the configuration for an enterprise.
                :param enterprise_id: The ID of the enterprise.
        Example: "3442311"
                :type enterprise_id: str
                :param categories: A comma-separated list of the enterprise configuration categories.
        Allowed values: `security`, `content_and_sharing`, `user_settings`, `shield`.
                :type categories: List[str]
                :param box_version: Version header., defaults to BoxVersionHeaderV2025R0._2025_0
                :type box_version: BoxVersionHeaderV2025R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {'categories': to_string(categories)}
        )
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/enterprise_configurations/',
                        to_string(enterprise_id),
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
        return deserialize(response.data, EnterpriseConfigurationV2025R0)
