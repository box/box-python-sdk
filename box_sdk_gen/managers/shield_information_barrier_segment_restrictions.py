from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.shield_information_barrier_segment_restriction import (
    ShieldInformationBarrierSegmentRestriction,
)

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.shield_information_barrier_segment_restrictions import (
    ShieldInformationBarrierSegmentRestrictions,
)

from box_sdk_gen.schemas.shield_information_barrier_base import (
    ShieldInformationBarrierBase,
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


class CreateShieldInformationBarrierSegmentRestrictionType(str, Enum):
    SHIELD_INFORMATION_BARRIER_SEGMENT_RESTRICTION = (
        'shield_information_barrier_segment_restriction'
    )


class CreateShieldInformationBarrierSegmentRestrictionShieldInformationBarrierSegmentTypeField(
    str, Enum
):
    SHIELD_INFORMATION_BARRIER_SEGMENT = 'shield_information_barrier_segment'


class CreateShieldInformationBarrierSegmentRestrictionShieldInformationBarrierSegment(
    BaseObject
):
    _discriminator = 'type', {'shield_information_barrier_segment'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[
            CreateShieldInformationBarrierSegmentRestrictionShieldInformationBarrierSegmentTypeField
        ] = None,
        **kwargs
    ):
        """
                :param id: The ID reference of the requesting
        shield information barrier segment., defaults to None
                :type id: Optional[str], optional
                :param type: The type of the shield barrier segment for this member., defaults to None
                :type type: Optional[CreateShieldInformationBarrierSegmentRestrictionShieldInformationBarrierSegmentTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class CreateShieldInformationBarrierSegmentRestrictionRestrictedSegmentTypeField(
    str, Enum
):
    SHIELD_INFORMATION_BARRIER_SEGMENT = 'shield_information_barrier_segment'


class CreateShieldInformationBarrierSegmentRestrictionRestrictedSegment(BaseObject):
    _discriminator = 'type', {'shield_information_barrier_segment'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[
            CreateShieldInformationBarrierSegmentRestrictionRestrictedSegmentTypeField
        ] = None,
        **kwargs
    ):
        """
                :param id: The ID reference of the restricted
        shield information barrier segment., defaults to None
                :type id: Optional[str], optional
                :param type: The type of the restricted shield
        information barrier segment., defaults to None
                :type type: Optional[CreateShieldInformationBarrierSegmentRestrictionRestrictedSegmentTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class ShieldInformationBarrierSegmentRestrictionsManager:
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

    def get_shield_information_barrier_segment_restriction_by_id(
        self,
        shield_information_barrier_segment_restriction_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShieldInformationBarrierSegmentRestriction:
        """
                Retrieves a shield information barrier segment

                restriction based on provided ID.

                :param shield_information_barrier_segment_restriction_id: The ID of the shield information barrier segment Restriction.
        Example: "4563"
                :type shield_information_barrier_segment_restriction_id: str
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
                        '/2.0/shield_information_barrier_segment_restrictions/',
                        to_string(shield_information_barrier_segment_restriction_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShieldInformationBarrierSegmentRestriction)

    def delete_shield_information_barrier_segment_restriction_by_id(
        self,
        shield_information_barrier_segment_restriction_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Delete shield information barrier segment restriction

                based on provided ID.

                :param shield_information_barrier_segment_restriction_id: The ID of the shield information barrier segment Restriction.
        Example: "4563"
                :type shield_information_barrier_segment_restriction_id: str
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
                        '/2.0/shield_information_barrier_segment_restrictions/',
                        to_string(shield_information_barrier_segment_restriction_id),
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

    def get_shield_information_barrier_segment_restrictions(
        self,
        shield_information_barrier_segment_id: str,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShieldInformationBarrierSegmentRestrictions:
        """
                Lists shield information barrier segment restrictions

                based on provided segment ID.

                :param shield_information_barrier_segment_id: The ID of the shield information barrier segment.
                :type shield_information_barrier_segment_id: str
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
            {
                'shield_information_barrier_segment_id': to_string(
                    shield_information_barrier_segment_id
                ),
                'marker': to_string(marker),
                'limit': to_string(limit),
            }
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shield_information_barrier_segment_restrictions',
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
        return deserialize(response.data, ShieldInformationBarrierSegmentRestrictions)

    def create_shield_information_barrier_segment_restriction(
        self,
        shield_information_barrier_segment: CreateShieldInformationBarrierSegmentRestrictionShieldInformationBarrierSegment,
        restricted_segment: CreateShieldInformationBarrierSegmentRestrictionRestrictedSegment,
        *,
        type: CreateShieldInformationBarrierSegmentRestrictionType = CreateShieldInformationBarrierSegmentRestrictionType.SHIELD_INFORMATION_BARRIER_SEGMENT_RESTRICTION,
        shield_information_barrier: Optional[ShieldInformationBarrierBase] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShieldInformationBarrierSegmentRestriction:
        """
                Creates a shield information barrier

                segment restriction object.

                :param shield_information_barrier_segment: The `type` and `id` of the requested
        shield information barrier segment.
                :type shield_information_barrier_segment: CreateShieldInformationBarrierSegmentRestrictionShieldInformationBarrierSegment
                :param restricted_segment: The `type` and `id` of the restricted
        shield information barrier segment.
                :type restricted_segment: CreateShieldInformationBarrierSegmentRestrictionRestrictedSegment
                :param type: The type of the shield barrier segment
        restriction for this member., defaults to CreateShieldInformationBarrierSegmentRestrictionType.SHIELD_INFORMATION_BARRIER_SEGMENT_RESTRICTION
                :type type: CreateShieldInformationBarrierSegmentRestrictionType, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'type': type,
            'shield_information_barrier': shield_information_barrier,
            'shield_information_barrier_segment': shield_information_barrier_segment,
            'restricted_segment': restricted_segment,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shield_information_barrier_segment_restrictions',
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
        return deserialize(response.data, ShieldInformationBarrierSegmentRestriction)
