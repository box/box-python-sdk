from enum import Enum

from typing import Optional

from typing import List

from typing import Dict

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.realtime_servers import RealtimeServers

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.events import Events

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import prepare_params

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.serialization.json import SerializedData

from box_sdk_gen.internal.utils import DateTime

from box_sdk_gen.serialization.json import sd_to_json

from box_sdk_gen.box.event_stream import EventStream


class GetEventsStreamType(str, Enum):
    ALL = 'all'
    CHANGES = 'changes'
    SYNC = 'sync'
    ADMIN_LOGS = 'admin_logs'
    ADMIN_LOGS_STREAMING = 'admin_logs_streaming'


class GetEventsEventType(str, Enum):
    ACCESS_GRANTED = 'ACCESS_GRANTED'
    ACCESS_REVOKED = 'ACCESS_REVOKED'
    ADD_DEVICE_ASSOCIATION = 'ADD_DEVICE_ASSOCIATION'
    ADD_LOGIN_ACTIVITY_DEVICE = 'ADD_LOGIN_ACTIVITY_DEVICE'
    ADMIN_LOGIN = 'ADMIN_LOGIN'
    APPLICATION_CREATED = 'APPLICATION_CREATED'
    APPLICATION_PUBLIC_KEY_ADDED = 'APPLICATION_PUBLIC_KEY_ADDED'
    APPLICATION_PUBLIC_KEY_DELETED = 'APPLICATION_PUBLIC_KEY_DELETED'
    CHANGE_ADMIN_ROLE = 'CHANGE_ADMIN_ROLE'
    CHANGE_FOLDER_PERMISSION = 'CHANGE_FOLDER_PERMISSION'
    COLLABORATION_ACCEPT = 'COLLABORATION_ACCEPT'
    COLLABORATION_EXPIRATION = 'COLLABORATION_EXPIRATION'
    COLLABORATION_INVITE = 'COLLABORATION_INVITE'
    COLLABORATION_REMOVE = 'COLLABORATION_REMOVE'
    COLLABORATION_ROLE_CHANGE = 'COLLABORATION_ROLE_CHANGE'
    COMMENT_CREATE = 'COMMENT_CREATE'
    COMMENT_DELETE = 'COMMENT_DELETE'
    CONTENT_WORKFLOW_ABNORMAL_DOWNLOAD_ACTIVITY = (
        'CONTENT_WORKFLOW_ABNORMAL_DOWNLOAD_ACTIVITY'
    )
    CONTENT_WORKFLOW_AUTOMATION_ADD = 'CONTENT_WORKFLOW_AUTOMATION_ADD'
    CONTENT_WORKFLOW_AUTOMATION_DELETE = 'CONTENT_WORKFLOW_AUTOMATION_DELETE'
    CONTENT_WORKFLOW_POLICY_ADD = 'CONTENT_WORKFLOW_POLICY_ADD'
    CONTENT_WORKFLOW_SHARING_POLICY_VIOLATION = (
        'CONTENT_WORKFLOW_SHARING_POLICY_VIOLATION'
    )
    CONTENT_WORKFLOW_UPLOAD_POLICY_VIOLATION = (
        'CONTENT_WORKFLOW_UPLOAD_POLICY_VIOLATION'
    )
    COPY = 'COPY'
    DATA_RETENTION_CREATE_RETENTION = 'DATA_RETENTION_CREATE_RETENTION'
    DATA_RETENTION_REMOVE_RETENTION = 'DATA_RETENTION_REMOVE_RETENTION'
    DELETE = 'DELETE'
    DELETE_USER = 'DELETE_USER'
    DEVICE_TRUST_CHECK_FAILED = 'DEVICE_TRUST_CHECK_FAILED'
    DOWNLOAD = 'DOWNLOAD'
    EDIT = 'EDIT'
    EDIT_USER = 'EDIT_USER'
    EMAIL_ALIAS_CONFIRM = 'EMAIL_ALIAS_CONFIRM'
    EMAIL_ALIAS_REMOVE = 'EMAIL_ALIAS_REMOVE'
    ENTERPRISE_APP_AUTHORIZATION_UPDATE = 'ENTERPRISE_APP_AUTHORIZATION_UPDATE'
    EXTERNAL_COLLAB_SECURITY_SETTINGS = 'EXTERNAL_COLLAB_SECURITY_SETTINGS'
    FAILED_LOGIN = 'FAILED_LOGIN'
    FILE_MARKED_MALICIOUS = 'FILE_MARKED_MALICIOUS'
    FILE_WATERMARKED_DOWNLOAD = 'FILE_WATERMARKED_DOWNLOAD'
    GROUP_ADD_ITEM = 'GROUP_ADD_ITEM'
    GROUP_ADD_USER = 'GROUP_ADD_USER'
    GROUP_CREATION = 'GROUP_CREATION'
    GROUP_DELETION = 'GROUP_DELETION'
    GROUP_EDITED = 'GROUP_EDITED'
    GROUP_REMOVE_ITEM = 'GROUP_REMOVE_ITEM'
    GROUP_REMOVE_USER = 'GROUP_REMOVE_USER'
    ITEM_EMAIL_SEND = 'ITEM_EMAIL_SEND'
    ITEM_MODIFY = 'ITEM_MODIFY'
    ITEM_OPEN = 'ITEM_OPEN'
    ITEM_SHARED_UPDATE = 'ITEM_SHARED_UPDATE'
    ITEM_SYNC = 'ITEM_SYNC'
    ITEM_UNSYNC = 'ITEM_UNSYNC'
    LEGAL_HOLD_ASSIGNMENT_CREATE = 'LEGAL_HOLD_ASSIGNMENT_CREATE'
    LEGAL_HOLD_ASSIGNMENT_DELETE = 'LEGAL_HOLD_ASSIGNMENT_DELETE'
    LEGAL_HOLD_POLICY_CREATE = 'LEGAL_HOLD_POLICY_CREATE'
    LEGAL_HOLD_POLICY_DELETE = 'LEGAL_HOLD_POLICY_DELETE'
    LEGAL_HOLD_POLICY_UPDATE = 'LEGAL_HOLD_POLICY_UPDATE'
    LOCK = 'LOCK'
    LOGIN = 'LOGIN'
    METADATA_INSTANCE_CREATE = 'METADATA_INSTANCE_CREATE'
    METADATA_INSTANCE_DELETE = 'METADATA_INSTANCE_DELETE'
    METADATA_INSTANCE_UPDATE = 'METADATA_INSTANCE_UPDATE'
    METADATA_TEMPLATE_CREATE = 'METADATA_TEMPLATE_CREATE'
    METADATA_TEMPLATE_DELETE = 'METADATA_TEMPLATE_DELETE'
    METADATA_TEMPLATE_UPDATE = 'METADATA_TEMPLATE_UPDATE'
    MOVE = 'MOVE'
    NEW_USER = 'NEW_USER'
    OAUTH2_ACCESS_TOKEN_REVOKE = 'OAUTH2_ACCESS_TOKEN_REVOKE'
    PREVIEW = 'PREVIEW'
    REMOVE_DEVICE_ASSOCIATION = 'REMOVE_DEVICE_ASSOCIATION'
    REMOVE_LOGIN_ACTIVITY_DEVICE = 'REMOVE_LOGIN_ACTIVITY_DEVICE'
    RENAME = 'RENAME'
    RETENTION_POLICY_ASSIGNMENT_ADD = 'RETENTION_POLICY_ASSIGNMENT_ADD'
    SHARE = 'SHARE'
    SHARED_LINK_SEND = 'SHARED_LINK_SEND'
    SHARE_EXPIRATION = 'SHARE_EXPIRATION'
    SHIELD_ALERT = 'SHIELD_ALERT'
    SHIELD_EXTERNAL_COLLAB_ACCESS_BLOCKED = 'SHIELD_EXTERNAL_COLLAB_ACCESS_BLOCKED'
    SHIELD_EXTERNAL_COLLAB_ACCESS_BLOCKED_MISSING_JUSTIFICATION = (
        'SHIELD_EXTERNAL_COLLAB_ACCESS_BLOCKED_MISSING_JUSTIFICATION'
    )
    SHIELD_EXTERNAL_COLLAB_INVITE_BLOCKED = 'SHIELD_EXTERNAL_COLLAB_INVITE_BLOCKED'
    SHIELD_EXTERNAL_COLLAB_INVITE_BLOCKED_MISSING_JUSTIFICATION = (
        'SHIELD_EXTERNAL_COLLAB_INVITE_BLOCKED_MISSING_JUSTIFICATION'
    )
    SHIELD_JUSTIFICATION_APPROVAL = 'SHIELD_JUSTIFICATION_APPROVAL'
    SHIELD_SHARED_LINK_ACCESS_BLOCKED = 'SHIELD_SHARED_LINK_ACCESS_BLOCKED'
    SHIELD_SHARED_LINK_STATUS_RESTRICTED_ON_CREATE = (
        'SHIELD_SHARED_LINK_STATUS_RESTRICTED_ON_CREATE'
    )
    SHIELD_SHARED_LINK_STATUS_RESTRICTED_ON_UPDATE = (
        'SHIELD_SHARED_LINK_STATUS_RESTRICTED_ON_UPDATE'
    )
    SIGN_DOCUMENT_ASSIGNED = 'SIGN_DOCUMENT_ASSIGNED'
    SIGN_DOCUMENT_CANCELLED = 'SIGN_DOCUMENT_CANCELLED'
    SIGN_DOCUMENT_COMPLETED = 'SIGN_DOCUMENT_COMPLETED'
    SIGN_DOCUMENT_CONVERTED = 'SIGN_DOCUMENT_CONVERTED'
    SIGN_DOCUMENT_CREATED = 'SIGN_DOCUMENT_CREATED'
    SIGN_DOCUMENT_DECLINED = 'SIGN_DOCUMENT_DECLINED'
    SIGN_DOCUMENT_EXPIRED = 'SIGN_DOCUMENT_EXPIRED'
    SIGN_DOCUMENT_SIGNED = 'SIGN_DOCUMENT_SIGNED'
    SIGN_DOCUMENT_VIEWED_BY_SIGNED = 'SIGN_DOCUMENT_VIEWED_BY_SIGNED'
    SIGNER_DOWNLOADED = 'SIGNER_DOWNLOADED'
    SIGNER_FORWARDED = 'SIGNER_FORWARDED'
    STORAGE_EXPIRATION = 'STORAGE_EXPIRATION'
    TASK_ASSIGNMENT_CREATE = 'TASK_ASSIGNMENT_CREATE'
    TASK_ASSIGNMENT_DELETE = 'TASK_ASSIGNMENT_DELETE'
    TASK_ASSIGNMENT_UPDATE = 'TASK_ASSIGNMENT_UPDATE'
    TASK_CREATE = 'TASK_CREATE'
    TASK_UPDATE = 'TASK_UPDATE'
    TERMS_OF_SERVICE_ACCEPT = 'TERMS_OF_SERVICE_ACCEPT'
    TERMS_OF_SERVICE_REJECT = 'TERMS_OF_SERVICE_REJECT'
    UNDELETE = 'UNDELETE'
    UNLOCK = 'UNLOCK'
    UNSHARE = 'UNSHARE'
    UPDATE_COLLABORATION_EXPIRATION = 'UPDATE_COLLABORATION_EXPIRATION'
    UPDATE_SHARE_EXPIRATION = 'UPDATE_SHARE_EXPIRATION'
    UPLOAD = 'UPLOAD'
    USER_AUTHENTICATE_OAUTH2_ACCESS_TOKEN_CREATE = (
        'USER_AUTHENTICATE_OAUTH2_ACCESS_TOKEN_CREATE'
    )
    WATERMARK_LABEL_CREATE = 'WATERMARK_LABEL_CREATE'
    WATERMARK_LABEL_DELETE = 'WATERMARK_LABEL_DELETE'


class GetEventStreamQueryParamsStreamTypeField(str, Enum):
    ALL = 'all'
    CHANGES = 'changes'
    SYNC = 'sync'
    ADMIN_LOGS = 'admin_logs'
    ADMIN_LOGS_STREAMING = 'admin_logs_streaming'


class GetEventStreamQueryParamsEventTypeField(str, Enum):
    ACCESS_GRANTED = 'ACCESS_GRANTED'
    ACCESS_REVOKED = 'ACCESS_REVOKED'
    ADD_DEVICE_ASSOCIATION = 'ADD_DEVICE_ASSOCIATION'
    ADD_LOGIN_ACTIVITY_DEVICE = 'ADD_LOGIN_ACTIVITY_DEVICE'
    ADMIN_LOGIN = 'ADMIN_LOGIN'
    APPLICATION_CREATED = 'APPLICATION_CREATED'
    APPLICATION_PUBLIC_KEY_ADDED = 'APPLICATION_PUBLIC_KEY_ADDED'
    APPLICATION_PUBLIC_KEY_DELETED = 'APPLICATION_PUBLIC_KEY_DELETED'
    CHANGE_ADMIN_ROLE = 'CHANGE_ADMIN_ROLE'
    CHANGE_FOLDER_PERMISSION = 'CHANGE_FOLDER_PERMISSION'
    COLLABORATION_ACCEPT = 'COLLABORATION_ACCEPT'
    COLLABORATION_EXPIRATION = 'COLLABORATION_EXPIRATION'
    COLLABORATION_INVITE = 'COLLABORATION_INVITE'
    COLLABORATION_REMOVE = 'COLLABORATION_REMOVE'
    COLLABORATION_ROLE_CHANGE = 'COLLABORATION_ROLE_CHANGE'
    COMMENT_CREATE = 'COMMENT_CREATE'
    COMMENT_DELETE = 'COMMENT_DELETE'
    CONTENT_WORKFLOW_ABNORMAL_DOWNLOAD_ACTIVITY = (
        'CONTENT_WORKFLOW_ABNORMAL_DOWNLOAD_ACTIVITY'
    )
    CONTENT_WORKFLOW_AUTOMATION_ADD = 'CONTENT_WORKFLOW_AUTOMATION_ADD'
    CONTENT_WORKFLOW_AUTOMATION_DELETE = 'CONTENT_WORKFLOW_AUTOMATION_DELETE'
    CONTENT_WORKFLOW_POLICY_ADD = 'CONTENT_WORKFLOW_POLICY_ADD'
    CONTENT_WORKFLOW_SHARING_POLICY_VIOLATION = (
        'CONTENT_WORKFLOW_SHARING_POLICY_VIOLATION'
    )
    CONTENT_WORKFLOW_UPLOAD_POLICY_VIOLATION = (
        'CONTENT_WORKFLOW_UPLOAD_POLICY_VIOLATION'
    )
    COPY = 'COPY'
    DATA_RETENTION_CREATE_RETENTION = 'DATA_RETENTION_CREATE_RETENTION'
    DATA_RETENTION_REMOVE_RETENTION = 'DATA_RETENTION_REMOVE_RETENTION'
    DELETE = 'DELETE'
    DELETE_USER = 'DELETE_USER'
    DEVICE_TRUST_CHECK_FAILED = 'DEVICE_TRUST_CHECK_FAILED'
    DOWNLOAD = 'DOWNLOAD'
    EDIT = 'EDIT'
    EDIT_USER = 'EDIT_USER'
    EMAIL_ALIAS_CONFIRM = 'EMAIL_ALIAS_CONFIRM'
    EMAIL_ALIAS_REMOVE = 'EMAIL_ALIAS_REMOVE'
    ENTERPRISE_APP_AUTHORIZATION_UPDATE = 'ENTERPRISE_APP_AUTHORIZATION_UPDATE'
    EXTERNAL_COLLAB_SECURITY_SETTINGS = 'EXTERNAL_COLLAB_SECURITY_SETTINGS'
    FAILED_LOGIN = 'FAILED_LOGIN'
    FILE_MARKED_MALICIOUS = 'FILE_MARKED_MALICIOUS'
    FILE_WATERMARKED_DOWNLOAD = 'FILE_WATERMARKED_DOWNLOAD'
    GROUP_ADD_ITEM = 'GROUP_ADD_ITEM'
    GROUP_ADD_USER = 'GROUP_ADD_USER'
    GROUP_CREATION = 'GROUP_CREATION'
    GROUP_DELETION = 'GROUP_DELETION'
    GROUP_EDITED = 'GROUP_EDITED'
    GROUP_REMOVE_ITEM = 'GROUP_REMOVE_ITEM'
    GROUP_REMOVE_USER = 'GROUP_REMOVE_USER'
    ITEM_EMAIL_SEND = 'ITEM_EMAIL_SEND'
    ITEM_MODIFY = 'ITEM_MODIFY'
    ITEM_OPEN = 'ITEM_OPEN'
    ITEM_SHARED_UPDATE = 'ITEM_SHARED_UPDATE'
    ITEM_SYNC = 'ITEM_SYNC'
    ITEM_UNSYNC = 'ITEM_UNSYNC'
    LEGAL_HOLD_ASSIGNMENT_CREATE = 'LEGAL_HOLD_ASSIGNMENT_CREATE'
    LEGAL_HOLD_ASSIGNMENT_DELETE = 'LEGAL_HOLD_ASSIGNMENT_DELETE'
    LEGAL_HOLD_POLICY_CREATE = 'LEGAL_HOLD_POLICY_CREATE'
    LEGAL_HOLD_POLICY_DELETE = 'LEGAL_HOLD_POLICY_DELETE'
    LEGAL_HOLD_POLICY_UPDATE = 'LEGAL_HOLD_POLICY_UPDATE'
    LOCK = 'LOCK'
    LOGIN = 'LOGIN'
    METADATA_INSTANCE_CREATE = 'METADATA_INSTANCE_CREATE'
    METADATA_INSTANCE_DELETE = 'METADATA_INSTANCE_DELETE'
    METADATA_INSTANCE_UPDATE = 'METADATA_INSTANCE_UPDATE'
    METADATA_TEMPLATE_CREATE = 'METADATA_TEMPLATE_CREATE'
    METADATA_TEMPLATE_DELETE = 'METADATA_TEMPLATE_DELETE'
    METADATA_TEMPLATE_UPDATE = 'METADATA_TEMPLATE_UPDATE'
    MOVE = 'MOVE'
    NEW_USER = 'NEW_USER'
    OAUTH2_ACCESS_TOKEN_REVOKE = 'OAUTH2_ACCESS_TOKEN_REVOKE'
    PREVIEW = 'PREVIEW'
    REMOVE_DEVICE_ASSOCIATION = 'REMOVE_DEVICE_ASSOCIATION'
    REMOVE_LOGIN_ACTIVITY_DEVICE = 'REMOVE_LOGIN_ACTIVITY_DEVICE'
    RENAME = 'RENAME'
    RETENTION_POLICY_ASSIGNMENT_ADD = 'RETENTION_POLICY_ASSIGNMENT_ADD'
    SHARE = 'SHARE'
    SHARED_LINK_SEND = 'SHARED_LINK_SEND'
    SHARE_EXPIRATION = 'SHARE_EXPIRATION'
    SHIELD_ALERT = 'SHIELD_ALERT'
    SHIELD_EXTERNAL_COLLAB_ACCESS_BLOCKED = 'SHIELD_EXTERNAL_COLLAB_ACCESS_BLOCKED'
    SHIELD_EXTERNAL_COLLAB_ACCESS_BLOCKED_MISSING_JUSTIFICATION = (
        'SHIELD_EXTERNAL_COLLAB_ACCESS_BLOCKED_MISSING_JUSTIFICATION'
    )
    SHIELD_EXTERNAL_COLLAB_INVITE_BLOCKED = 'SHIELD_EXTERNAL_COLLAB_INVITE_BLOCKED'
    SHIELD_EXTERNAL_COLLAB_INVITE_BLOCKED_MISSING_JUSTIFICATION = (
        'SHIELD_EXTERNAL_COLLAB_INVITE_BLOCKED_MISSING_JUSTIFICATION'
    )
    SHIELD_JUSTIFICATION_APPROVAL = 'SHIELD_JUSTIFICATION_APPROVAL'
    SHIELD_SHARED_LINK_ACCESS_BLOCKED = 'SHIELD_SHARED_LINK_ACCESS_BLOCKED'
    SHIELD_SHARED_LINK_STATUS_RESTRICTED_ON_CREATE = (
        'SHIELD_SHARED_LINK_STATUS_RESTRICTED_ON_CREATE'
    )
    SHIELD_SHARED_LINK_STATUS_RESTRICTED_ON_UPDATE = (
        'SHIELD_SHARED_LINK_STATUS_RESTRICTED_ON_UPDATE'
    )
    SIGN_DOCUMENT_ASSIGNED = 'SIGN_DOCUMENT_ASSIGNED'
    SIGN_DOCUMENT_CANCELLED = 'SIGN_DOCUMENT_CANCELLED'
    SIGN_DOCUMENT_COMPLETED = 'SIGN_DOCUMENT_COMPLETED'
    SIGN_DOCUMENT_CONVERTED = 'SIGN_DOCUMENT_CONVERTED'
    SIGN_DOCUMENT_CREATED = 'SIGN_DOCUMENT_CREATED'
    SIGN_DOCUMENT_DECLINED = 'SIGN_DOCUMENT_DECLINED'
    SIGN_DOCUMENT_EXPIRED = 'SIGN_DOCUMENT_EXPIRED'
    SIGN_DOCUMENT_SIGNED = 'SIGN_DOCUMENT_SIGNED'
    SIGN_DOCUMENT_VIEWED_BY_SIGNED = 'SIGN_DOCUMENT_VIEWED_BY_SIGNED'
    SIGNER_DOWNLOADED = 'SIGNER_DOWNLOADED'
    SIGNER_FORWARDED = 'SIGNER_FORWARDED'
    STORAGE_EXPIRATION = 'STORAGE_EXPIRATION'
    TASK_ASSIGNMENT_CREATE = 'TASK_ASSIGNMENT_CREATE'
    TASK_ASSIGNMENT_DELETE = 'TASK_ASSIGNMENT_DELETE'
    TASK_ASSIGNMENT_UPDATE = 'TASK_ASSIGNMENT_UPDATE'
    TASK_CREATE = 'TASK_CREATE'
    TASK_UPDATE = 'TASK_UPDATE'
    TERMS_OF_SERVICE_ACCEPT = 'TERMS_OF_SERVICE_ACCEPT'
    TERMS_OF_SERVICE_REJECT = 'TERMS_OF_SERVICE_REJECT'
    UNDELETE = 'UNDELETE'
    UNLOCK = 'UNLOCK'
    UNSHARE = 'UNSHARE'
    UPDATE_COLLABORATION_EXPIRATION = 'UPDATE_COLLABORATION_EXPIRATION'
    UPDATE_SHARE_EXPIRATION = 'UPDATE_SHARE_EXPIRATION'
    UPLOAD = 'UPLOAD'
    USER_AUTHENTICATE_OAUTH2_ACCESS_TOKEN_CREATE = (
        'USER_AUTHENTICATE_OAUTH2_ACCESS_TOKEN_CREATE'
    )
    WATERMARK_LABEL_CREATE = 'WATERMARK_LABEL_CREATE'
    WATERMARK_LABEL_DELETE = 'WATERMARK_LABEL_DELETE'


class GetEventStreamQueryParams:
    def __init__(
        self,
        *,
        stream_type: Optional[GetEventStreamQueryParamsStreamTypeField] = None,
        stream_position: Optional[str] = None,
        limit: Optional[int] = None,
        event_type: Optional[List[GetEventStreamQueryParamsEventTypeField]] = None,
        created_after: Optional[DateTime] = None,
        created_before: Optional[DateTime] = None
    ):
        """
                :param stream_type: Defines the type of events that are returned

        * `all` returns everything for a user and is the default
        * `changes` returns events that may cause file tree changes
          such as file updates or collaborations.
        * `sync` is similar to `changes` but only applies to synced folders
        * `admin_logs` returns all events for an entire enterprise and
          requires the user making the API call to have admin permissions. This
          stream type is for programmatically pulling from a 1 year history of
          events across all users within the enterprise and within a
          `created_after` and `created_before` time frame. The complete history
          of events will be returned in chronological order based on the event
          time, but latency will be much higher than `admin_logs_streaming`.
        * `admin_logs_streaming` returns all events for an entire enterprise and
          requires the user making the API call to have admin permissions. This
          stream type is for polling for recent events across all users within
          the enterprise. Latency will be much lower than `admin_logs`, but
          events will not be returned in chronological order and may
          contain duplicates., defaults to None
                :type stream_type: Optional[GetEventStreamQueryParamsStreamTypeField], optional
                :param stream_position: The location in the event stream to start receiving events from.

        * `now` will return an empty list events and
        the latest stream position for initialization.
        * `0` or `null` will return all events., defaults to None
                :type stream_position: Optional[str], optional
                :param limit: Limits the number of events returned.

        Note: Sometimes, the events less than the limit requested can be returned
        even when there may be more events remaining. This is primarily done in
        the case where a number of events have already been retrieved and these
        retrieved events are returned rather than delaying for an unknown amount
        of time to see if there are any more results., defaults to None
                :type limit: Optional[int], optional
                :param event_type: A comma-separated list of events to filter by. This can only be used when
        requesting the events with a `stream_type` of `admin_logs` or
        `adming_logs_streaming`. For any other `stream_type` this value will be
        ignored., defaults to None
                :type event_type: Optional[List[GetEventStreamQueryParamsEventTypeField]], optional
                :param created_after: The lower bound date and time to return events for. This can only be used
        when requesting the events with a `stream_type` of `admin_logs`. For any
        other `stream_type` this value will be ignored., defaults to None
                :type created_after: Optional[DateTime], optional
                :param created_before: The upper bound date and time to return events for. This can only be used
        when requesting the events with a `stream_type` of `admin_logs`. For any
        other `stream_type` this value will be ignored., defaults to None
                :type created_before: Optional[DateTime], optional
        """
        self.stream_type = stream_type
        self.stream_position = stream_position
        self.limit = limit
        self.event_type = event_type
        self.created_after = created_after
        self.created_before = created_before


class GetEventStreamHeaders:
    def __init__(self, *, extra_headers: Optional[Dict[str, Optional[str]]] = None):
        """
        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        self.extra_headers = extra_headers


class EventsManager:
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

    def get_events_with_long_polling(
        self, *, extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> RealtimeServers:
        """
        Returns a list of real-time servers that can be used for long-polling updates

        to the [event stream](#get-events).


        Long polling is the concept where a HTTP request is kept open until the


        server sends a response, then repeating the process over and over to receive


        updated responses.


        Long polling the event stream can only be used for user events, not for


        enterprise events.


        To use long polling, first use this endpoint to retrieve a list of long poll


        URLs. Next, make a long poll request to any of the provided URLs.


        When an event occurs in monitored account a response with the value


        `new_change` will be sent. The response contains no other details as


        it only serves as a prompt to take further action such as sending a


        request to the [events endpoint](#get-events) with the last known


        `stream_position`.


        After the server sends this response it closes the connection. You must now


        repeat the long poll process to begin listening for events again.


        If no events occur for a while and the connection times out you will


        receive a response with the value `reconnect`. When you receive this response


        you’ll make another call to this endpoint to restart the process.


        If you receive no events in `retry_timeout` seconds then you will need to


        make another request to the real-time server (one of the URLs in the response


        for this endpoint). This might be necessary due to network errors.


        Finally, if you receive a `max_retries` error when making a request to the


        real-time server, you should start over by making a call to this endpoint


        first.

        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join([self.network_session.base_urls.base_url, '/2.0/events']),
                method='OPTIONS',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, RealtimeServers)

    def get_events(
        self,
        *,
        stream_type: Optional[GetEventsStreamType] = None,
        stream_position: Optional[str] = None,
        limit: Optional[int] = None,
        event_type: Optional[List[GetEventsEventType]] = None,
        created_after: Optional[DateTime] = None,
        created_before: Optional[DateTime] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Events:
        """
                Returns up to a year of past events for a given user

                or for the entire enterprise.


                By default this returns events for the authenticated user. To retrieve events


                for the entire enterprise, set the `stream_type` to `admin_logs_streaming`


                for live monitoring of new events, or `admin_logs` for querying across


                historical events. The user making the API call will


                need to have admin privileges, and the application will need to have the


                scope `manage enterprise properties` checked.

                :param stream_type: Defines the type of events that are returned

        * `all` returns everything for a user and is the default
        * `changes` returns events that may cause file tree changes
          such as file updates or collaborations.
        * `sync` is similar to `changes` but only applies to synced folders
        * `admin_logs` returns all events for an entire enterprise and
          requires the user making the API call to have admin permissions. This
          stream type is for programmatically pulling from a 1 year history of
          events across all users within the enterprise and within a
          `created_after` and `created_before` time frame. The complete history
          of events will be returned in chronological order based on the event
          time, but latency will be much higher than `admin_logs_streaming`.
        * `admin_logs_streaming` returns all events for an entire enterprise and
          requires the user making the API call to have admin permissions. This
          stream type is for polling for recent events across all users within
          the enterprise. Latency will be much lower than `admin_logs`, but
          events will not be returned in chronological order and may
          contain duplicates., defaults to None
                :type stream_type: Optional[GetEventsStreamType], optional
                :param stream_position: The location in the event stream to start receiving events from.

        * `now` will return an empty list events and
        the latest stream position for initialization.
        * `0` or `null` will return all events., defaults to None
                :type stream_position: Optional[str], optional
                :param limit: Limits the number of events returned.

        Note: Sometimes, the events less than the limit requested can be returned
        even when there may be more events remaining. This is primarily done in
        the case where a number of events have already been retrieved and these
        retrieved events are returned rather than delaying for an unknown amount
        of time to see if there are any more results., defaults to None
                :type limit: Optional[int], optional
                :param event_type: A comma-separated list of events to filter by. This can only be used when
        requesting the events with a `stream_type` of `admin_logs` or
        `adming_logs_streaming`. For any other `stream_type` this value will be
        ignored., defaults to None
                :type event_type: Optional[List[GetEventsEventType]], optional
                :param created_after: The lower bound date and time to return events for. This can only be used
        when requesting the events with a `stream_type` of `admin_logs`. For any
        other `stream_type` this value will be ignored., defaults to None
                :type created_after: Optional[DateTime], optional
                :param created_before: The upper bound date and time to return events for. This can only be used
        when requesting the events with a `stream_type` of `admin_logs`. For any
        other `stream_type` this value will be ignored., defaults to None
                :type created_before: Optional[DateTime], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'stream_type': to_string(stream_type),
                'stream_position': to_string(stream_position),
                'limit': to_string(limit),
                'event_type': to_string(event_type),
                'created_after': to_string(created_after),
                'created_before': to_string(created_before),
            }
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join([self.network_session.base_urls.base_url, '/2.0/events']),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, Events)

    def get_event_stream(
        self,
        *,
        query_params: GetEventStreamQueryParams = None,
        headers: GetEventStreamHeaders = None
    ) -> EventStream:
        """
        Get an event stream for the Box API
        :param query_params: Query parameters of getEvents method, defaults to None
        :type query_params: GetEventStreamQueryParams, optional
        :param headers: Headers of getEvents method, defaults to None
        :type headers: GetEventStreamHeaders, optional
        """
        if query_params is None:
            query_params = GetEventStreamQueryParams()
        if headers is None:
            headers = GetEventStreamHeaders()
        return EventStream(
            events_manager=self, query_params=query_params, headers_input=headers
        )
