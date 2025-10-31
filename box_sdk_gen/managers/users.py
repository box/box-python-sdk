from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.internal.null_value import NullValue

from typing import Union

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.users import Users

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.user_full import UserFull

from box_sdk_gen.schemas.tracking_code import TrackingCode

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


class GetUsersUserType(str, Enum):
    ALL = 'all'
    MANAGED = 'managed'
    EXTERNAL = 'external'


class CreateUserRole(str, Enum):
    COADMIN = 'coadmin'
    USER = 'user'


class CreateUserStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    CANNOT_DELETE_EDIT = 'cannot_delete_edit'
    CANNOT_DELETE_EDIT_UPLOAD = 'cannot_delete_edit_upload'


class UpdateUserByIdRole(str, Enum):
    COADMIN = 'coadmin'
    USER = 'user'


class UpdateUserByIdStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    CANNOT_DELETE_EDIT = 'cannot_delete_edit'
    CANNOT_DELETE_EDIT_UPLOAD = 'cannot_delete_edit_upload'


class UpdateUserByIdNotificationEmail(BaseObject):
    def __init__(self, *, email: Optional[str] = None, **kwargs):
        """
        :param email: The email address to send the notifications to., defaults to None
        :type email: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.email = email


class UsersManager:
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

    def get_users(
        self,
        *,
        filter_term: Optional[str] = None,
        user_type: Optional[GetUsersUserType] = None,
        external_app_user_id: Optional[str] = None,
        fields: Optional[List[str]] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        usemarker: Optional[bool] = None,
        marker: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Users:
        """
                Returns a list of all users for the Enterprise along with their `user_id`,

                `public_name`, and `login`.


                The application and the authenticated user need to


                have the permission to look up users in the entire


                enterprise.

                :param filter_term: Limits the results to only users who's `name` or
        `login` start with the search term.

        For externally managed users, the search term needs
        to completely match the in order to find the user, and
        it will only return one user at a time., defaults to None
                :type filter_term: Optional[str], optional
                :param user_type: Limits the results to the kind of user specified.

        * `all` returns every kind of user for whom the
          `login` or `name` partially matches the
          `filter_term`. It will only return an external user
          if the login matches the `filter_term` completely,
          and in that case it will only return that user.
        * `managed` returns all managed and app users for whom
          the `login` or `name` partially matches the
          `filter_term`.
        * `external` returns all external users for whom the
          `login` matches the `filter_term` exactly., defaults to None
                :type user_type: Optional[GetUsersUserType], optional
                :param external_app_user_id: Limits the results to app users with the given
        `external_app_user_id` value.

        When creating an app user, an
        `external_app_user_id` value can be set. This value can
        then be used in this endpoint to find any users that
        match that `external_app_user_id` value., defaults to None
                :type external_app_user_id: Optional[str], optional
                :param fields: A comma-separated list of attributes to include in the
        response. This can be used to request fields that are
        not normally returned in a standard response.

        Be aware that specifying this parameter will have the
        effect that none of the standard fields are returned in
        the response unless explicitly specified, instead only
        fields for the mini representation are returned, additional
        to the fields requested., defaults to None
                :type fields: Optional[List[str]], optional
                :param offset: The offset of the item at which to begin the response.

        Queries with offset parameter value
        exceeding 10000 will be rejected
        with a 400 response., defaults to None
                :type offset: Optional[int], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param usemarker: Specifies whether to use marker-based pagination instead of
        offset-based pagination. Only one pagination method can
        be used at a time.

        By setting this value to true, the API will return a `marker` field
        that can be passed as a parameter to this endpoint to get the next
        page of the response., defaults to None
                :type usemarker: Optional[bool], optional
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'filter_term': to_string(filter_term),
                'user_type': to_string(user_type),
                'external_app_user_id': to_string(external_app_user_id),
                'fields': to_string(fields),
                'offset': to_string(offset),
                'limit': to_string(limit),
                'usemarker': to_string(usemarker),
                'marker': to_string(marker),
            }
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join([self.network_session.base_urls.base_url, '/2.0/users']),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, Users)

    def create_user(
        self,
        name: str,
        *,
        login: Optional[str] = None,
        is_platform_access_only: Optional[bool] = None,
        role: Optional[CreateUserRole] = None,
        language: Optional[str] = None,
        is_sync_enabled: Optional[bool] = None,
        job_title: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        space_amount: Optional[int] = None,
        tracking_codes: Optional[List[TrackingCode]] = None,
        can_see_managed_users: Optional[bool] = None,
        timezone: Optional[str] = None,
        is_external_collab_restricted: Optional[bool] = None,
        is_exempt_from_device_limits: Optional[bool] = None,
        is_exempt_from_login_verification: Optional[bool] = None,
        status: Optional[CreateUserStatus] = None,
        external_app_user_id: Optional[str] = None,
        fields: Optional[List[str]] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> UserFull:
        """
                Creates a new managed user in an enterprise. This endpoint

                is only available to users and applications with the right


                admin permissions.

                :param name: The name of the user.
                :type name: str
                :param login: The email address the user uses to log in

        Required, unless `is_platform_access_only`
        is set to `true`., defaults to None
                :type login: Optional[str], optional
                :param is_platform_access_only: Specifies that the user is an app user., defaults to None
                :type is_platform_access_only: Optional[bool], optional
                :param role: The user’s enterprise role., defaults to None
                :type role: Optional[CreateUserRole], optional
                :param language: The language of the user, formatted in modified version of the
        [ISO 639-1](/guides/api-calls/language-codes) format., defaults to None
                :type language: Optional[str], optional
                :param is_sync_enabled: Whether the user can use Box Sync., defaults to None
                :type is_sync_enabled: Optional[bool], optional
                :param job_title: The user’s job title., defaults to None
                :type job_title: Optional[str], optional
                :param phone: The user’s phone number., defaults to None
                :type phone: Optional[str], optional
                :param address: The user’s address., defaults to None
                :type address: Optional[str], optional
                :param space_amount: The user’s total available space in bytes. Set this to `-1` to
        indicate unlimited storage., defaults to None
                :type space_amount: Optional[int], optional
                :param tracking_codes: Tracking codes allow an admin to generate reports from the
        admin console and assign an attribute to a specific group
        of users. This setting must be enabled for an enterprise before it
        can be used., defaults to None
                :type tracking_codes: Optional[List[TrackingCode]], optional
                :param can_see_managed_users: Whether the user can see other enterprise users in their
        contact list., defaults to None
                :type can_see_managed_users: Optional[bool], optional
                :param timezone: The user's timezone., defaults to None
                :type timezone: Optional[str], optional
                :param is_external_collab_restricted: Whether the user is allowed to collaborate with users outside
        their enterprise., defaults to None
                :type is_external_collab_restricted: Optional[bool], optional
                :param is_exempt_from_device_limits: Whether to exempt the user from enterprise device limits., defaults to None
                :type is_exempt_from_device_limits: Optional[bool], optional
                :param is_exempt_from_login_verification: Whether the user must use two-factor authentication., defaults to None
                :type is_exempt_from_login_verification: Optional[bool], optional
                :param status: The user's account status., defaults to None
                :type status: Optional[CreateUserStatus], optional
                :param external_app_user_id: An external identifier for an app user, which can be used to look
        up the user. This can be used to tie user IDs from external
        identity providers to Box users., defaults to None
                :type external_app_user_id: Optional[str], optional
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
            'login': login,
            'is_platform_access_only': is_platform_access_only,
            'role': role,
            'language': language,
            'is_sync_enabled': is_sync_enabled,
            'job_title': job_title,
            'phone': phone,
            'address': address,
            'space_amount': space_amount,
            'tracking_codes': tracking_codes,
            'can_see_managed_users': can_see_managed_users,
            'timezone': timezone,
            'is_external_collab_restricted': is_external_collab_restricted,
            'is_exempt_from_device_limits': is_exempt_from_device_limits,
            'is_exempt_from_login_verification': is_exempt_from_login_verification,
            'status': status,
            'external_app_user_id': external_app_user_id,
        }
        query_params_map: Dict[str, str] = prepare_params({'fields': to_string(fields)})
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join([self.network_session.base_urls.base_url, '/2.0/users']),
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
        return deserialize(response.data, UserFull)

    def get_user_me(
        self,
        *,
        fields: Optional[List[str]] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> UserFull:
        """
                Retrieves information about the user who is currently authenticated.

                In the case of a client-side authenticated OAuth 2.0 application


                this will be the user who authorized the app.


                In the case of a JWT, server-side authenticated application


                this will be the service account that belongs to the application


                by default.


                Use the `As-User` header to change who this API call is made on behalf of.

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
                url=''.join([self.network_session.base_urls.base_url, '/2.0/users/me']),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, UserFull)

    def get_user_by_id(
        self,
        user_id: str,
        *,
        fields: Optional[List[str]] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> UserFull:
        """
                Retrieves information about a user in the enterprise.

                The application and the authenticated user need to


                have the permission to look up users in the entire


                enterprise.


                This endpoint also returns a limited set of information


                for external users who are collaborated on content


                owned by the enterprise for authenticated users with the


                right scopes. In this case, disallowed fields will return


                null instead.

                :param user_id: The ID of the user.
        Example: "12345"
                :type user_id: str
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
                        '/2.0/users/',
                        to_string(user_id),
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
        return deserialize(response.data, UserFull)

    def update_user_by_id(
        self,
        user_id: str,
        *,
        enterprise: Union[Optional[str], NullValue] = None,
        notify: Optional[bool] = None,
        name: Optional[str] = None,
        login: Optional[str] = None,
        role: Optional[UpdateUserByIdRole] = None,
        language: Optional[str] = None,
        is_sync_enabled: Optional[bool] = None,
        job_title: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        tracking_codes: Optional[List[TrackingCode]] = None,
        can_see_managed_users: Optional[bool] = None,
        timezone: Optional[str] = None,
        is_external_collab_restricted: Optional[bool] = None,
        is_exempt_from_device_limits: Optional[bool] = None,
        is_exempt_from_login_verification: Optional[bool] = None,
        is_password_reset_required: Optional[bool] = None,
        status: Optional[UpdateUserByIdStatus] = None,
        space_amount: Optional[int] = None,
        notification_email: Union[
            Optional[UpdateUserByIdNotificationEmail], NullValue
        ] = None,
        external_app_user_id: Optional[str] = None,
        fields: Optional[List[str]] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> UserFull:
        """
                Updates a managed or app user in an enterprise. This endpoint

                is only available to users and applications with the right


                admin permissions.

                :param user_id: The ID of the user.
        Example: "12345"
                :type user_id: str
                :param enterprise: Set this to `null` to roll the user out of the enterprise
        and make them a free user., defaults to None
                :type enterprise: Union[Optional[str], NullValue], optional
                :param notify: Whether the user should receive an email when they
        are rolled out of an enterprise., defaults to None
                :type notify: Optional[bool], optional
                :param name: The name of the user., defaults to None
                :type name: Optional[str], optional
                :param login: The email address the user uses to log in

        Note: If the target user's email is not confirmed, then the
        primary login address cannot be changed., defaults to None
                :type login: Optional[str], optional
                :param role: The user’s enterprise role., defaults to None
                :type role: Optional[UpdateUserByIdRole], optional
                :param language: The language of the user, formatted in modified version of the
        [ISO 639-1](/guides/api-calls/language-codes) format., defaults to None
                :type language: Optional[str], optional
                :param is_sync_enabled: Whether the user can use Box Sync., defaults to None
                :type is_sync_enabled: Optional[bool], optional
                :param job_title: The user’s job title., defaults to None
                :type job_title: Optional[str], optional
                :param phone: The user’s phone number., defaults to None
                :type phone: Optional[str], optional
                :param address: The user’s address., defaults to None
                :type address: Optional[str], optional
                :param tracking_codes: Tracking codes allow an admin to generate reports from the
        admin console and assign an attribute to a specific group
        of users. This setting must be enabled for an enterprise before it
        can be used., defaults to None
                :type tracking_codes: Optional[List[TrackingCode]], optional
                :param can_see_managed_users: Whether the user can see other enterprise users in their
        contact list., defaults to None
                :type can_see_managed_users: Optional[bool], optional
                :param timezone: The user's timezone., defaults to None
                :type timezone: Optional[str], optional
                :param is_external_collab_restricted: Whether the user is allowed to collaborate with users outside
        their enterprise., defaults to None
                :type is_external_collab_restricted: Optional[bool], optional
                :param is_exempt_from_device_limits: Whether to exempt the user from enterprise device limits., defaults to None
                :type is_exempt_from_device_limits: Optional[bool], optional
                :param is_exempt_from_login_verification: Whether the user must use two-factor authentication., defaults to None
                :type is_exempt_from_login_verification: Optional[bool], optional
                :param is_password_reset_required: Whether the user is required to reset their password., defaults to None
                :type is_password_reset_required: Optional[bool], optional
                :param status: The user's account status., defaults to None
                :type status: Optional[UpdateUserByIdStatus], optional
                :param space_amount: The user’s total available space in bytes. Set this to `-1` to
        indicate unlimited storage., defaults to None
                :type space_amount: Optional[int], optional
                :param notification_email: An alternate notification email address to which email
        notifications are sent. When it's confirmed, this will be
        the email address to which notifications are sent instead of
        to the primary email address.

        Set this value to `null` to remove the notification email., defaults to None
                :type notification_email: Union[Optional[UpdateUserByIdNotificationEmail], NullValue], optional
                :param external_app_user_id: An external identifier for an app user, which can be used to look
        up the user. This can be used to tie user IDs from external
        identity providers to Box users.

        Note: In order to update this field, you need to request a token
        using the application that created the app user., defaults to None
                :type external_app_user_id: Optional[str], optional
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
            'notify': notify,
            'name': name,
            'login': login,
            'role': role,
            'language': language,
            'is_sync_enabled': is_sync_enabled,
            'job_title': job_title,
            'phone': phone,
            'address': address,
            'tracking_codes': tracking_codes,
            'can_see_managed_users': can_see_managed_users,
            'timezone': timezone,
            'is_external_collab_restricted': is_external_collab_restricted,
            'is_exempt_from_device_limits': is_exempt_from_device_limits,
            'is_exempt_from_login_verification': is_exempt_from_login_verification,
            'is_password_reset_required': is_password_reset_required,
            'status': status,
            'space_amount': space_amount,
            'notification_email': notification_email,
            'external_app_user_id': external_app_user_id,
        }
        query_params_map: Dict[str, str] = prepare_params({'fields': to_string(fields)})
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/users/',
                        to_string(user_id),
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
        return deserialize(response.data, UserFull)

    def delete_user_by_id(
        self,
        user_id: str,
        *,
        notify: Optional[bool] = None,
        force: Optional[bool] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Deletes a user. By default, this operation fails if the user

                still owns any content, was recently active, or recently joined the enterprise from a free account.


                To proceed, move their owned content first, or use the `force` parameter to delete


                the user and their files.

                :param user_id: The ID of the user.
        Example: "12345"
                :type user_id: str
                :param notify: Whether the user will receive email notification of
        the deletion., defaults to None
                :type notify: Optional[bool], optional
                :param force: Specifies whether to delete the user even if they still own files,
        were recently active, or recently joined the enterprise from a free account., defaults to None
                :type force: Optional[bool], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {'notify': to_string(notify), 'force': to_string(force)}
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/users/',
                        to_string(user_id),
                    ]
                ),
                method='DELETE',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None
