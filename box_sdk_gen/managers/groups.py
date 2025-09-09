from enum import Enum

from typing import Optional

from typing import List

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.groups import Groups

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.group_full import GroupFull

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


class CreateGroupInvitabilityLevel(str, Enum):
    ADMINS_ONLY = 'admins_only'
    ADMINS_AND_MEMBERS = 'admins_and_members'
    ALL_MANAGED_USERS = 'all_managed_users'


class CreateGroupMemberViewabilityLevel(str, Enum):
    ADMINS_ONLY = 'admins_only'
    ADMINS_AND_MEMBERS = 'admins_and_members'
    ALL_MANAGED_USERS = 'all_managed_users'


class UpdateGroupByIdInvitabilityLevel(str, Enum):
    ADMINS_ONLY = 'admins_only'
    ADMINS_AND_MEMBERS = 'admins_and_members'
    ALL_MANAGED_USERS = 'all_managed_users'


class UpdateGroupByIdMemberViewabilityLevel(str, Enum):
    ADMINS_ONLY = 'admins_only'
    ADMINS_AND_MEMBERS = 'admins_and_members'
    ALL_MANAGED_USERS = 'all_managed_users'


class GroupsManager:
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

    def get_groups(
        self,
        *,
        filter_term: Optional[str] = None,
        fields: Optional[List[str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Groups:
        """
                Retrieves all of the groups for a given enterprise. The user

                must have admin permissions to inspect enterprise's groups.

                :param filter_term: Limits the results to only groups whose `name` starts
        with the search term., defaults to None
                :type filter_term: Optional[str], optional
                :param fields: A comma-separated list of attributes to include in the
        response. This can be used to request fields that are
        not normally returned in a standard response.

        Be aware that specifying this parameter will have the
        effect that none of the standard fields are returned in
        the response unless explicitly specified, instead only
        fields for the mini representation are returned, additional
        to the fields requested., defaults to None
                :type fields: Optional[List[str]], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param offset: The offset of the item at which to begin the response.

        Queries with offset parameter value
        exceeding 10000 will be rejected
        with a 400 response., defaults to None
                :type offset: Optional[int], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'filter_term': to_string(filter_term),
                'fields': to_string(fields),
                'limit': to_string(limit),
                'offset': to_string(offset),
            }
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join([self.network_session.base_urls.base_url, '/2.0/groups']),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, Groups)

    def create_group(
        self,
        name: str,
        *,
        provenance: Optional[str] = None,
        external_sync_identifier: Optional[str] = None,
        description: Optional[str] = None,
        invitability_level: Optional[CreateGroupInvitabilityLevel] = None,
        member_viewability_level: Optional[CreateGroupMemberViewabilityLevel] = None,
        fields: Optional[List[str]] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> GroupFull:
        """
                Creates a new group of users in an enterprise. Only users with admin

                permissions can create new groups.

                :param name: The name of the new group to be created. This name must be unique
        within the enterprise.
                :type name: str
                :param provenance: Keeps track of which external source this group is
        coming, for example `Active Directory`, or `Okta`.

        Setting this will also prevent Box admins from editing
        the group name and its members directly via the Box
        web application.

        This is desirable for one-way syncing of groups., defaults to None
                :type provenance: Optional[str], optional
                :param external_sync_identifier: An arbitrary identifier that can be used by
        external group sync tools to link this Box Group to
        an external group.

        Example values of this field
        could be an **Active Directory Object ID** or a **Google
        Group ID**.

        We recommend you use of this field in
        order to avoid issues when group names are updated in
        either Box or external systems., defaults to None
                :type external_sync_identifier: Optional[str], optional
                :param description: A human readable description of the group., defaults to None
                :type description: Optional[str], optional
                :param invitability_level: Specifies who can invite the group to collaborate
        on folders.

        When set to `admins_only` the enterprise admin, co-admins,
        and the group's admin can invite the group.

        When set to `admins_and_members` all the admins listed
        above and group members can invite the group.

        When set to `all_managed_users` all managed users in the
        enterprise can invite the group., defaults to None
                :type invitability_level: Optional[CreateGroupInvitabilityLevel], optional
                :param member_viewability_level: Specifies who can see the members of the group.

        * `admins_only` - the enterprise admin, co-admins, group's
          group admin.
        * `admins_and_members` - all admins and group members.
        * `all_managed_users` - all managed users in the
          enterprise., defaults to None
                :type member_viewability_level: Optional[CreateGroupMemberViewabilityLevel], optional
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
            'name': name,
            'provenance': provenance,
            'external_sync_identifier': external_sync_identifier,
            'description': description,
            'invitability_level': invitability_level,
            'member_viewability_level': member_viewability_level,
        }
        query_params_map: Dict[str, str] = prepare_params({'fields': to_string(fields)})
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join([self.network_session.base_urls.base_url, '/2.0/groups']),
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
        return deserialize(response.data, GroupFull)

    def get_group_by_id(
        self,
        group_id: str,
        *,
        fields: Optional[List[str]] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> GroupFull:
        """
                Retrieves information about a group. Only members of this

                group or users with admin-level permissions will be able to


                use this API.

                :param group_id: The ID of the group.
        Example: "57645"
                :type group_id: str
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
                        '/2.0/groups/',
                        to_string(group_id),
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
        return deserialize(response.data, GroupFull)

    def update_group_by_id(
        self,
        group_id: str,
        *,
        name: Optional[str] = None,
        provenance: Optional[str] = None,
        external_sync_identifier: Optional[str] = None,
        description: Optional[str] = None,
        invitability_level: Optional[UpdateGroupByIdInvitabilityLevel] = None,
        member_viewability_level: Optional[
            UpdateGroupByIdMemberViewabilityLevel
        ] = None,
        fields: Optional[List[str]] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> GroupFull:
        """
                Updates a specific group. Only admins of this

                group or users with admin-level permissions will be able to


                use this API.

                :param group_id: The ID of the group.
        Example: "57645"
                :type group_id: str
                :param name: The name of the new group to be created. Must be unique within the
        enterprise., defaults to None
                :type name: Optional[str], optional
                :param provenance: Keeps track of which external source this group is
        coming, for example `Active Directory`, or `Okta`.

        Setting this will also prevent Box admins from editing
        the group name and its members directly via the Box
        web application.

        This is desirable for one-way syncing of groups., defaults to None
                :type provenance: Optional[str], optional
                :param external_sync_identifier: An arbitrary identifier that can be used by
        external group sync tools to link this Box Group to
        an external group.

        Example values of this field
        could be an **Active Directory Object ID** or a **Google
        Group ID**.

        We recommend you use of this field in
        order to avoid issues when group names are updated in
        either Box or external systems., defaults to None
                :type external_sync_identifier: Optional[str], optional
                :param description: A human readable description of the group., defaults to None
                :type description: Optional[str], optional
                :param invitability_level: Specifies who can invite the group to collaborate
        on folders.

        When set to `admins_only` the enterprise admin, co-admins,
        and the group's admin can invite the group.

        When set to `admins_and_members` all the admins listed
        above and group members can invite the group.

        When set to `all_managed_users` all managed users in the
        enterprise can invite the group., defaults to None
                :type invitability_level: Optional[UpdateGroupByIdInvitabilityLevel], optional
                :param member_viewability_level: Specifies who can see the members of the group.

        * `admins_only` - the enterprise admin, co-admins, group's
          group admin.
        * `admins_and_members` - all admins and group members.
        * `all_managed_users` - all managed users in the
          enterprise., defaults to None
                :type member_viewability_level: Optional[UpdateGroupByIdMemberViewabilityLevel], optional
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
            'name': name,
            'provenance': provenance,
            'external_sync_identifier': external_sync_identifier,
            'description': description,
            'invitability_level': invitability_level,
            'member_viewability_level': member_viewability_level,
        }
        query_params_map: Dict[str, str] = prepare_params({'fields': to_string(fields)})
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/groups/',
                        to_string(group_id),
                    ]
                ),
                method='PUT',
                params=query_params_map,
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, GroupFull)

    def delete_group_by_id(
        self, group_id: str, *, extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Permanently deletes a group. Only users with

                admin-level permissions will be able to use this API.

                :param group_id: The ID of the group.
        Example: "57645"
                :type group_id: str
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
                        '/2.0/groups/',
                        to_string(group_id),
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
