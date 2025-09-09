from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from typing import Optional

from typing import List

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.legal_hold_policy_assignments import LegalHoldPolicyAssignments

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.legal_hold_policy_assignment import LegalHoldPolicyAssignment

from box_sdk_gen.schemas.files_on_hold import FilesOnHold

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


class GetLegalHoldPolicyAssignmentsAssignToType(str, Enum):
    FILE = 'file'
    FILE_VERSION = 'file_version'
    FOLDER = 'folder'
    USER = 'user'
    OWNERSHIP = 'ownership'
    INTERACTIONS = 'interactions'


class CreateLegalHoldPolicyAssignmentAssignToTypeField(str, Enum):
    FILE = 'file'
    FILE_VERSION = 'file_version'
    FOLDER = 'folder'
    USER = 'user'
    OWNERSHIP = 'ownership'
    INTERACTION = 'interaction'


class CreateLegalHoldPolicyAssignmentAssignTo(BaseObject):
    _discriminator = 'type', {
        'file',
        'file_version',
        'folder',
        'user',
        'ownership',
        'interaction',
    }

    def __init__(
        self, type: CreateLegalHoldPolicyAssignmentAssignToTypeField, id: str, **kwargs
    ):
        """
        :param type: The type of item to assign the policy to.
        :type type: CreateLegalHoldPolicyAssignmentAssignToTypeField
        :param id: The ID of item to assign the policy to.
        :type id: str
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id


class LegalHoldPolicyAssignmentsManager:
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

    def get_legal_hold_policy_assignments(
        self,
        policy_id: str,
        *,
        assign_to_type: Optional[GetLegalHoldPolicyAssignmentsAssignToType] = None,
        assign_to_id: Optional[str] = None,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        fields: Optional[List[str]] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> LegalHoldPolicyAssignments:
        """
                Retrieves a list of items a legal hold policy has been assigned to.
                :param policy_id: The ID of the legal hold policy.
                :type policy_id: str
                :param assign_to_type: Filters the results by the type of item the
        policy was applied to., defaults to None
                :type assign_to_type: Optional[GetLegalHoldPolicyAssignmentsAssignToType], optional
                :param assign_to_id: Filters the results by the ID of item the
        policy was applied to., defaults to None
                :type assign_to_id: Optional[str], optional
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
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
        query_params_map: Dict[str, str] = prepare_params(
            {
                'policy_id': to_string(policy_id),
                'assign_to_type': to_string(assign_to_type),
                'assign_to_id': to_string(assign_to_id),
                'marker': to_string(marker),
                'limit': to_string(limit),
                'fields': to_string(fields),
            }
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/legal_hold_policy_assignments',
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
        return deserialize(response.data, LegalHoldPolicyAssignments)

    def create_legal_hold_policy_assignment(
        self,
        policy_id: str,
        assign_to: CreateLegalHoldPolicyAssignmentAssignTo,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> LegalHoldPolicyAssignment:
        """
        Assign a legal hold to a file, file version, folder, or user.
        :param policy_id: The ID of the policy to assign.
        :type policy_id: str
        :param assign_to: The item to assign the policy to.
        :type assign_to: CreateLegalHoldPolicyAssignmentAssignTo
        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'policy_id': policy_id, 'assign_to': assign_to}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/legal_hold_policy_assignments',
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
        return deserialize(response.data, LegalHoldPolicyAssignment)

    def get_legal_hold_policy_assignment_by_id(
        self,
        legal_hold_policy_assignment_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> LegalHoldPolicyAssignment:
        """
                Retrieve a legal hold policy assignment.
                :param legal_hold_policy_assignment_id: The ID of the legal hold policy assignment.
        Example: "753465"
                :type legal_hold_policy_assignment_id: str
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
                        '/2.0/legal_hold_policy_assignments/',
                        to_string(legal_hold_policy_assignment_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, LegalHoldPolicyAssignment)

    def delete_legal_hold_policy_assignment_by_id(
        self,
        legal_hold_policy_assignment_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Remove a legal hold from an item.

                This is an asynchronous process. The policy will not be


                fully removed yet when the response returns.

                :param legal_hold_policy_assignment_id: The ID of the legal hold policy assignment.
        Example: "753465"
                :type legal_hold_policy_assignment_id: str
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
                        '/2.0/legal_hold_policy_assignments/',
                        to_string(legal_hold_policy_assignment_id),
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

    def get_legal_hold_policy_assignment_file_on_hold(
        self,
        legal_hold_policy_assignment_id: str,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        fields: Optional[List[str]] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> FilesOnHold:
        """
                Get a list of files with current file versions for a legal hold

                assignment.


                In some cases you may want to get previous file versions instead. In these


                cases, use the `GET  /legal_hold_policy_assignments/:id/file_versions_on_hold`


                API instead to return any previous versions of a file for this legal hold


                policy assignment.


                Due to ongoing re-architecture efforts this API might not return all file


                versions held for this policy ID. Instead, this API will only return the


                latest file version held in the newly developed architecture. The `GET


                /file_version_legal_holds` API can be used to fetch current and past versions


                of files held within the legacy architecture.


                This endpoint does not support returning any content that is on hold due to


                a Custodian collaborating on a Hub.


                The `GET /legal_hold_policy_assignments?policy_id={id}` API can be used to


                find a list of policy assignments for a given policy ID.

                :param legal_hold_policy_assignment_id: The ID of the legal hold policy assignment.
        Example: "753465"
                :type legal_hold_policy_assignment_id: str
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
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
        query_params_map: Dict[str, str] = prepare_params(
            {
                'marker': to_string(marker),
                'limit': to_string(limit),
                'fields': to_string(fields),
            }
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/legal_hold_policy_assignments/',
                        to_string(legal_hold_policy_assignment_id),
                        '/files_on_hold',
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
        return deserialize(response.data, FilesOnHold)
