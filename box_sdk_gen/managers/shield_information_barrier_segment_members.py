from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.shield_information_barrier_segment_member import (
    ShieldInformationBarrierSegmentMember,
)

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.shield_information_barrier_segment_members import (
    ShieldInformationBarrierSegmentMembers,
)

from box_sdk_gen.schemas.shield_information_barrier_base import (
    ShieldInformationBarrierBase,
)

from box_sdk_gen.schemas.user_base import UserBase

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


class CreateShieldInformationBarrierSegmentMemberType(str, Enum):
    SHIELD_INFORMATION_BARRIER_SEGMENT_MEMBER = (
        'shield_information_barrier_segment_member'
    )


class CreateShieldInformationBarrierSegmentMemberShieldInformationBarrierSegmentTypeField(
    str, Enum
):
    SHIELD_INFORMATION_BARRIER_SEGMENT = 'shield_information_barrier_segment'


class CreateShieldInformationBarrierSegmentMemberShieldInformationBarrierSegment(
    BaseObject
):
    _discriminator = 'type', {'shield_information_barrier_segment'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[
            CreateShieldInformationBarrierSegmentMemberShieldInformationBarrierSegmentTypeField
        ] = None,
        **kwargs
    ):
        """
                :param id: The ID reference of the
        requesting shield information barrier segment., defaults to None
                :type id: Optional[str], optional
                :param type: The type of the shield barrier segment for this member., defaults to None
                :type type: Optional[CreateShieldInformationBarrierSegmentMemberShieldInformationBarrierSegmentTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class ShieldInformationBarrierSegmentMembersManager:
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

    def get_shield_information_barrier_segment_member_by_id(
        self,
        shield_information_barrier_segment_member_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShieldInformationBarrierSegmentMember:
        """
                Retrieves a shield information barrier

                segment member by its ID.

                :param shield_information_barrier_segment_member_id: The ID of the shield information barrier segment Member.
        Example: "7815"
                :type shield_information_barrier_segment_member_id: str
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
                        '/2.0/shield_information_barrier_segment_members/',
                        to_string(shield_information_barrier_segment_member_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ShieldInformationBarrierSegmentMember)

    def delete_shield_information_barrier_segment_member_by_id(
        self,
        shield_information_barrier_segment_member_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Deletes a shield information barrier

                segment member based on provided ID.

                :param shield_information_barrier_segment_member_id: The ID of the shield information barrier segment Member.
        Example: "7815"
                :type shield_information_barrier_segment_member_id: str
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
                        '/2.0/shield_information_barrier_segment_members/',
                        to_string(shield_information_barrier_segment_member_id),
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

    def get_shield_information_barrier_segment_members(
        self,
        shield_information_barrier_segment_id: str,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShieldInformationBarrierSegmentMembers:
        """
                Lists shield information barrier segment members

                based on provided segment IDs.

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
                        '/2.0/shield_information_barrier_segment_members',
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
        return deserialize(response.data, ShieldInformationBarrierSegmentMembers)

    def create_shield_information_barrier_segment_member(
        self,
        shield_information_barrier_segment: CreateShieldInformationBarrierSegmentMemberShieldInformationBarrierSegment,
        user: UserBase,
        *,
        type: Optional[CreateShieldInformationBarrierSegmentMemberType] = None,
        shield_information_barrier: Optional[ShieldInformationBarrierBase] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ShieldInformationBarrierSegmentMember:
        """
                Creates a new shield information barrier segment member.
                :param shield_information_barrier_segment: The `type` and `id` of the
        requested shield information barrier segment.
                :type shield_information_barrier_segment: CreateShieldInformationBarrierSegmentMemberShieldInformationBarrierSegment
                :param user: User to which restriction will be applied.
                :type user: UserBase
                :param type: A type of the shield barrier segment member., defaults to None
                :type type: Optional[CreateShieldInformationBarrierSegmentMemberType], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'type': type,
            'shield_information_barrier': shield_information_barrier,
            'shield_information_barrier_segment': shield_information_barrier_segment,
            'user': user,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/shield_information_barrier_segment_members',
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
        return deserialize(response.data, ShieldInformationBarrierSegmentMember)
