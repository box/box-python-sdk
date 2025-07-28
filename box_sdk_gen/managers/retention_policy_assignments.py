from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.retention_policy_assignments import RetentionPolicyAssignments

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.retention_policy_assignment import RetentionPolicyAssignment

from box_sdk_gen.schemas.files_under_retention import FilesUnderRetention

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


class GetRetentionPolicyAssignmentsType(str, Enum):
    FOLDER = 'folder'
    ENTERPRISE = 'enterprise'
    METADATA_TEMPLATE = 'metadata_template'


class CreateRetentionPolicyAssignmentAssignToTypeField(str, Enum):
    ENTERPRISE = 'enterprise'
    FOLDER = 'folder'
    METADATA_TEMPLATE = 'metadata_template'


class CreateRetentionPolicyAssignmentAssignTo(BaseObject):
    _discriminator = 'type', {'enterprise', 'folder', 'metadata_template'}

    def __init__(
        self,
        type: CreateRetentionPolicyAssignmentAssignToTypeField,
        *,
        id: Optional[str] = None,
        **kwargs
    ):
        """
                :param type: The type of item to assign the policy to.
                :type type: CreateRetentionPolicyAssignmentAssignToTypeField
                :param id: The ID of item to assign the policy to.
        Set to `null` or omit when `type` is set to
        `enterprise`., defaults to None
                :type id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id


class CreateRetentionPolicyAssignmentFilterFields(BaseObject):
    def __init__(
        self, *, field: Optional[str] = None, value: Optional[str] = None, **kwargs
    ):
        """
                :param field: The metadata attribute key id., defaults to None
                :type field: Optional[str], optional
                :param value: The metadata attribute field id. For value, only
        enum and multiselect types are supported., defaults to None
                :type value: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.field = field
        self.value = value


class RetentionPolicyAssignmentsManager:
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

    def get_retention_policy_assignments(
        self,
        retention_policy_id: str,
        *,
        type: Optional[GetRetentionPolicyAssignmentsType] = None,
        fields: Optional[List[str]] = None,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> RetentionPolicyAssignments:
        """
                Returns a list of all retention policy assignments associated with a specified

                retention policy.

                :param retention_policy_id: The ID of the retention policy.
        Example: "982312"
                :type retention_policy_id: str
                :param type: The type of the retention policy assignment to retrieve., defaults to None
                :type type: Optional[GetRetentionPolicyAssignmentsType], optional
                :param fields: A comma-separated list of attributes to include in the
        response. This can be used to request fields that are
        not normally returned in a standard response.

        Be aware that specifying this parameter will have the
        effect that none of the standard fields are returned in
        the response unless explicitly specified, instead only
        fields for the mini representation are returned, additional
        to the fields requested., defaults to None
                :type fields: Optional[List[str]], optional
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination., defaults to None
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
                'type': to_string(type),
                'fields': to_string(fields),
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
                        '/2.0/retention_policies/',
                        to_string(retention_policy_id),
                        '/assignments',
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
        return deserialize(response.data, RetentionPolicyAssignments)

    def create_retention_policy_assignment(
        self,
        policy_id: str,
        assign_to: CreateRetentionPolicyAssignmentAssignTo,
        *,
        filter_fields: Optional[
            List[CreateRetentionPolicyAssignmentFilterFields]
        ] = None,
        start_date_field: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> RetentionPolicyAssignment:
        """
                Assigns a retention policy to an item.
                :param policy_id: The ID of the retention policy to assign.
                :type policy_id: str
                :param assign_to: The item to assign the policy to.
                :type assign_to: CreateRetentionPolicyAssignmentAssignTo
                :param filter_fields: If the `assign_to` type is `metadata_template`,
        then optionally add the `filter_fields` parameter which will
        require an array of objects with a field entry and a value entry.
        Currently only one object of `field` and `value` is supported., defaults to None
                :type filter_fields: Optional[List[CreateRetentionPolicyAssignmentFilterFields]], optional
                :param start_date_field: The date the retention policy assignment begins.

        If the `assigned_to` type is `metadata_template`,
        this field can be a date field's metadata attribute key id., defaults to None
                :type start_date_field: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'policy_id': policy_id,
            'assign_to': assign_to,
            'filter_fields': filter_fields,
            'start_date_field': start_date_field,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/retention_policy_assignments',
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
        return deserialize(response.data, RetentionPolicyAssignment)

    def get_retention_policy_assignment_by_id(
        self,
        retention_policy_assignment_id: str,
        *,
        fields: Optional[List[str]] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> RetentionPolicyAssignment:
        """
                Retrieves a retention policy assignment.
                :param retention_policy_assignment_id: The ID of the retention policy assignment.
        Example: "1233123"
                :type retention_policy_assignment_id: str
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
                        '/2.0/retention_policy_assignments/',
                        to_string(retention_policy_assignment_id),
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
        return deserialize(response.data, RetentionPolicyAssignment)

    def delete_retention_policy_assignment_by_id(
        self,
        retention_policy_assignment_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Removes a retention policy assignment

                applied to content.

                :param retention_policy_assignment_id: The ID of the retention policy assignment.
        Example: "1233123"
                :type retention_policy_assignment_id: str
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
                        '/2.0/retention_policy_assignments/',
                        to_string(retention_policy_assignment_id),
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

    def get_files_under_retention_policy_assignment(
        self,
        retention_policy_assignment_id: str,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> FilesUnderRetention:
        """
                Returns a list of files under retention for a retention policy assignment.
                :param retention_policy_assignment_id: The ID of the retention policy assignment.
        Example: "1233123"
                :type retention_policy_assignment_id: str
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
            {'marker': to_string(marker), 'limit': to_string(limit)}
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/retention_policy_assignments/',
                        to_string(retention_policy_assignment_id),
                        '/files_under_retention',
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
        return deserialize(response.data, FilesUnderRetention)
