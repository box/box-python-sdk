from box_sdk_gen.internal.base_object import BaseObject

from typing import Optional

from typing import List

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.invite import Invite

from box_sdk_gen.schemas.client_error import ClientError

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


class CreateInviteEnterprise(BaseObject):
    def __init__(self, id: str, **kwargs):
        """
        :param id: The ID of the enterprise.
        :type id: str
        """
        super().__init__(**kwargs)
        self.id = id


class CreateInviteActionableBy(BaseObject):
    def __init__(self, *, login: Optional[str] = None, **kwargs):
        """
        :param login: The login of the invited user., defaults to None
        :type login: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.login = login


class InvitesManager:
    def __init__(
        self,
        *,
        auth: Optional[Authentication] = None,
        network_session: Optional[NetworkSession] = None
    ):
        if network_session is None:
            network_session = NetworkSession()
        self.auth = auth
        self.network_session = network_session

    def create_invite(
        self,
        enterprise: CreateInviteEnterprise,
        actionable_by: CreateInviteActionableBy,
        *,
        is_auto_roll_in_enabled: Optional[bool] = None,
        fields: Optional[List[str]] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Invite:
        """
                Invites an existing external user to join an enterprise.

                The user must already have a Box account and cannot be


                part of another enterprise. Once invited, the user receives


                an email and is prompted to accept the invitation in


                the Box web application.


                If `is_auto_roll_in_enabled` is set to `true`, the user does not have to


                accept the invitation and is added to the enterprise automatically after


                14 days. Only unmanaged users can be invited this way. An unmanaged user


                is a free user whose email domain matches one of the enterprise's


                domains. Availability depends on the enterprise's plan.


                This method requires the "Manage An Enterprise" scope enabled for


                the application, which can be enabled within the developer console.

                :param enterprise: The enterprise to invite the user to.
                :type enterprise: CreateInviteEnterprise
                :param actionable_by: The user to invite.
                :type actionable_by: CreateInviteActionableBy
                :param is_auto_roll_in_enabled: If set to `true`, the user is added to the enterprise
        automatically after 14 days instead of having to accept the
        invite. Only unmanaged users can be invited this way.
        Availability depends on the enterprise's plan., defaults to None
                :type is_auto_roll_in_enabled: Optional[bool], optional
                :param fields: A comma-separated list of attributes to include in the
        response. This can be used to request fields that are
        not normally returned in a standard response.

        Be aware that specifying this parameter will have the
        effect that none of the standard fields are returned in
        the response unless explicitly specified, instead only
        fields for the mini representation are returned, additional
        to the fields requested., defaults to None
                :type fields: Optional[List[str]], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'enterprise': enterprise,
            'actionable_by': actionable_by,
            'is_auto_roll_in_enabled': is_auto_roll_in_enabled,
        }
        query_params_map: Dict[str, str] = prepare_params({'fields': to_string(fields)})
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join([self.network_session.base_urls.base_url, '/2.0/invites']),
                method='POST',
                params=query_params_map,
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, Invite)

    def get_invite_by_id(
        self,
        invite_id: str,
        *,
        fields: Optional[List[str]] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Invite:
        """
                Returns the status of a user invite.
                :param invite_id: The ID of an invite.
        Example: "213723"
                :type invite_id: str
                :param fields: A comma-separated list of attributes to include in the
        response. This can be used to request fields that are
        not normally returned in a standard response.

        Be aware that specifying this parameter will have the
        effect that none of the standard fields are returned in
        the response unless explicitly specified, instead only
        fields for the mini representation are returned, additional
        to the fields requested., defaults to None
                :type fields: Optional[List[str]], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params({'fields': to_string(fields)})
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/invites/',
                        to_string(invite_id),
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
        return deserialize(response.data, Invite)
