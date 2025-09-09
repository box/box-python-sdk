from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.v2025_r0.shield_list_content_country_v2025_r0 import (
    ShieldListContentCountryV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.shield_list_content_domain_v2025_r0 import (
    ShieldListContentDomainV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.shield_list_content_email_v2025_r0 import (
    ShieldListContentEmailV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.shield_list_content_ip_v2025_r0 import (
    ShieldListContentIpV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.shield_list_content_request_v2025_r0 import (
    ShieldListContentRequestV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.shield_lists_v2025_r0 import ShieldListsV2025R0

from box_sdk_gen.parameters.v2025_r0.box_version_header_v2025_r0 import (
    BoxVersionHeaderV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.shield_list_v2025_r0 import ShieldListV2025R0

from box_sdk_gen.schemas.v2025_r0.client_error_v2025_r0 import ClientErrorV2025R0

from box_sdk_gen.schemas.v2025_r0.shield_lists_create_v2025_r0 import (
    ShieldListsCreateV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.shield_lists_update_v2025_r0 import (
    ShieldListsUpdateV2025R0,
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


class ShieldListsManager:
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

    def get_shield_lists_v2025_r0(
        self,
        *,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShieldListsV2025R0:
        """
        Retrieves all shield lists in the enterprise.
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
                    [self.network_session.base_urls.base_url, '/2.0/shield_lists']
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShieldListsV2025R0)

    def create_shield_list_v2025_r0(
        self,
        name: str,
        content: ShieldListContentRequestV2025R0,
        *,
        description: Optional[str] = None,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShieldListV2025R0:
        """
        Creates a shield list.
        :param name: The name of the shield list.
        :type name: str
        :param description: Optional description of Shield List., defaults to None
        :type description: Optional[str], optional
        :param box_version: Version header., defaults to BoxVersionHeaderV2025R0._2025_0
        :type box_version: BoxVersionHeaderV2025R0, optional
        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'name': name,
            'description': description,
            'content': content,
        }
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/shield_lists']
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
        return deserialize(response.data, ShieldListV2025R0)

    def get_shield_list_by_id_v2025_r0(
        self,
        shield_list_id: str,
        *,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShieldListV2025R0:
        """
                Retrieves a single shield list by its ID.
                :param shield_list_id: The unique identifier that represents a shield list.
        The ID for any Shield List can be determined by the response from the endpoint
        fetching all shield lists for the enterprise.
        Example: "90fb0e17-c332-40ed-b4f9-fa8908fbbb24 "
                :type shield_list_id: str
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
                        '/2.0/shield_lists/',
                        to_string(shield_list_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShieldListV2025R0)

    def delete_shield_list_by_id_v2025_r0(
        self,
        shield_list_id: str,
        *,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Delete a single shield list by its ID.
                :param shield_list_id: The unique identifier that represents a shield list.
        The ID for any Shield List can be determined by the response from the endpoint
        fetching all shield lists for the enterprise.
        Example: "90fb0e17-c332-40ed-b4f9-fa8908fbbb24 "
                :type shield_list_id: str
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
                        '/2.0/shield_lists/',
                        to_string(shield_list_id),
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

    def update_shield_list_by_id_v2025_r0(
        self,
        shield_list_id: str,
        name: str,
        content: ShieldListContentRequestV2025R0,
        *,
        description: Optional[str] = None,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShieldListV2025R0:
        """
                Updates a shield list.
                :param shield_list_id: The unique identifier that represents a shield list.
        The ID for any Shield List can be determined by the response from the endpoint
        fetching all shield lists for the enterprise.
        Example: "90fb0e17-c332-40ed-b4f9-fa8908fbbb24 "
                :type shield_list_id: str
                :param name: The name of the shield list.
                :type name: str
                :param description: Optional description of Shield List., defaults to None
                :type description: Optional[str], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2025R0._2025_0
                :type box_version: BoxVersionHeaderV2025R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'name': name,
            'description': description,
            'content': content,
        }
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shield_lists/',
                        to_string(shield_list_id),
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
        return deserialize(response.data, ShieldListV2025R0)
