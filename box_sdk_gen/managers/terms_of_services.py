from enum import Enum

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.terms_of_services import TermsOfServices

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.terms_of_service import TermsOfService

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


class GetTermsOfServiceTosType(str, Enum):
    EXTERNAL = 'external'
    MANAGED = 'managed'


class CreateTermsOfServiceStatus(str, Enum):
    ENABLED = 'enabled'
    DISABLED = 'disabled'


class CreateTermsOfServiceTosType(str, Enum):
    EXTERNAL = 'external'
    MANAGED = 'managed'


class UpdateTermsOfServiceByIdStatus(str, Enum):
    ENABLED = 'enabled'
    DISABLED = 'disabled'


class TermsOfServicesManager:
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

    def get_terms_of_service(
        self,
        *,
        tos_type: Optional[GetTermsOfServiceTosType] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> TermsOfServices:
        """
        Returns the current terms of service text and settings

        for the enterprise.

        :param tos_type: Limits the results to the terms of service of the given type., defaults to None
        :type tos_type: Optional[GetTermsOfServiceTosType], optional
        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {'tos_type': to_string(tos_type)}
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/terms_of_services']
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, TermsOfServices)

    def create_terms_of_service(
        self,
        status: CreateTermsOfServiceStatus,
        text: str,
        *,
        tos_type: Optional[CreateTermsOfServiceTosType] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> TermsOfService:
        """
                Creates a terms of service for a given enterprise

                and type of user.

                :param status: Whether this terms of service is active.
                :type status: CreateTermsOfServiceStatus
                :param text: The terms of service text to display to users.

        The text can be set to empty if the `status` is set to `disabled`.
                :type text: str
                :param tos_type: The type of user to set the terms of
        service for., defaults to None
                :type tos_type: Optional[CreateTermsOfServiceTosType], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'status': status, 'tos_type': tos_type, 'text': text}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/terms_of_services']
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
        return deserialize(response.data, TermsOfService)

    def get_terms_of_service_by_id(
        self,
        terms_of_service_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> TermsOfService:
        """
                Fetches a specific terms of service.
                :param terms_of_service_id: The ID of the terms of service.
        Example: "324234"
                :type terms_of_service_id: str
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
                        '/2.0/terms_of_services/',
                        to_string(terms_of_service_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, TermsOfService)

    def update_terms_of_service_by_id(
        self,
        terms_of_service_id: str,
        status: UpdateTermsOfServiceByIdStatus,
        text: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> TermsOfService:
        """
                Updates a specific terms of service.
                :param terms_of_service_id: The ID of the terms of service.
        Example: "324234"
                :type terms_of_service_id: str
                :param status: Whether this terms of service is active.
                :type status: UpdateTermsOfServiceByIdStatus
                :param text: The terms of service text to display to users.

        The text can be set to empty if the `status` is set to `disabled`.
                :type text: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'status': status, 'text': text}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/terms_of_services/',
                        to_string(terms_of_service_id),
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
        return deserialize(response.data, TermsOfService)
