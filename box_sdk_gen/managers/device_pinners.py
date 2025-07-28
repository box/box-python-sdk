from enum import Enum

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.device_pinner import DevicePinner

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.device_pinners import DevicePinners

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


class GetEnterpriseDevicePinnersDirection(str, Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class DevicePinnersManager:
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

    def get_device_pinner_by_id(
        self,
        device_pinner_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> DevicePinner:
        """
                Retrieves information about an individual device pin.
                :param device_pinner_id: The ID of the device pin.
        Example: "2324234"
                :type device_pinner_id: str
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
                        '/2.0/device_pinners/',
                        to_string(device_pinner_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, DevicePinner)

    def delete_device_pinner_by_id(
        self,
        device_pinner_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Deletes an individual device pin.
                :param device_pinner_id: The ID of the device pin.
        Example: "2324234"
                :type device_pinner_id: str
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
                        '/2.0/device_pinners/',
                        to_string(device_pinner_id),
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

    def get_enterprise_device_pinners(
        self,
        enterprise_id: str,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        direction: Optional[GetEnterpriseDevicePinnersDirection] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> DevicePinners:
        """
                Retrieves all the device pins within an enterprise.

                The user must have admin privileges, and the application


                needs the "manage enterprise" scope to make this call.

                :param enterprise_id: The ID of the enterprise.
        Example: "3442311"
                :type enterprise_id: str
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param direction: The direction to sort results in. This can be either in alphabetical ascending
        (`ASC`) or descending (`DESC`) order., defaults to None
                :type direction: Optional[GetEnterpriseDevicePinnersDirection], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'marker': to_string(marker),
                'limit': to_string(limit),
                'direction': to_string(direction),
            }
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/enterprises/',
                        to_string(enterprise_id),
                        '/device_pinners',
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
        return deserialize(response.data, DevicePinners)
