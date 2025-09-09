from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.storage_policy_assignments import StoragePolicyAssignments

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.storage_policy_assignment import StoragePolicyAssignment

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


class GetStoragePolicyAssignmentsResolvedForType(str, Enum):
    USER = 'user'
    ENTERPRISE = 'enterprise'


class CreateStoragePolicyAssignmentStoragePolicyTypeField(str, Enum):
    STORAGE_POLICY = 'storage_policy'


class CreateStoragePolicyAssignmentStoragePolicy(BaseObject):
    _discriminator = 'type', {'storage_policy'}

    def __init__(
        self,
        id: str,
        *,
        type: CreateStoragePolicyAssignmentStoragePolicyTypeField = CreateStoragePolicyAssignmentStoragePolicyTypeField.STORAGE_POLICY,
        **kwargs
    ):
        """
        :param id: The ID of the storage policy to assign.
        :type id: str
        :param type: The type to assign., defaults to CreateStoragePolicyAssignmentStoragePolicyTypeField.STORAGE_POLICY
        :type type: CreateStoragePolicyAssignmentStoragePolicyTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class CreateStoragePolicyAssignmentAssignedToTypeField(str, Enum):
    USER = 'user'
    ENTERPRISE = 'enterprise'


class CreateStoragePolicyAssignmentAssignedTo(BaseObject):
    _discriminator = 'type', {'user', 'enterprise'}

    def __init__(
        self, type: CreateStoragePolicyAssignmentAssignedToTypeField, id: str, **kwargs
    ):
        """
        :param type: The type to assign the policy to.
        :type type: CreateStoragePolicyAssignmentAssignedToTypeField
        :param id: The ID of the user or enterprise.
        :type id: str
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id


class UpdateStoragePolicyAssignmentByIdStoragePolicyTypeField(str, Enum):
    STORAGE_POLICY = 'storage_policy'


class UpdateStoragePolicyAssignmentByIdStoragePolicy(BaseObject):
    _discriminator = 'type', {'storage_policy'}

    def __init__(
        self,
        id: str,
        *,
        type: UpdateStoragePolicyAssignmentByIdStoragePolicyTypeField = UpdateStoragePolicyAssignmentByIdStoragePolicyTypeField.STORAGE_POLICY,
        **kwargs
    ):
        """
        :param id: The ID of the storage policy to assign.
        :type id: str
        :param type: The type to assign., defaults to UpdateStoragePolicyAssignmentByIdStoragePolicyTypeField.STORAGE_POLICY
        :type type: UpdateStoragePolicyAssignmentByIdStoragePolicyTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class StoragePolicyAssignmentsManager:
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

    def get_storage_policy_assignments(
        self,
        resolved_for_type: GetStoragePolicyAssignmentsResolvedForType,
        resolved_for_id: str,
        *,
        marker: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> StoragePolicyAssignments:
        """
                Fetches all the storage policy assignment for an enterprise or user.
                :param resolved_for_type: The target type to return assignments for.
                :type resolved_for_type: GetStoragePolicyAssignmentsResolvedForType
                :param resolved_for_id: The ID of the user or enterprise to return assignments for.
                :type resolved_for_id: str
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
                'marker': to_string(marker),
                'resolved_for_type': to_string(resolved_for_type),
                'resolved_for_id': to_string(resolved_for_id),
            }
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/storage_policy_assignments',
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
        return deserialize(response.data, StoragePolicyAssignments)

    def create_storage_policy_assignment(
        self,
        storage_policy: CreateStoragePolicyAssignmentStoragePolicy,
        assigned_to: CreateStoragePolicyAssignmentAssignedTo,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> StoragePolicyAssignment:
        """
                Creates a storage policy assignment for an enterprise or user.
                :param storage_policy: The storage policy to assign to the user or
        enterprise.
                :type storage_policy: CreateStoragePolicyAssignmentStoragePolicy
                :param assigned_to: The user or enterprise to assign the storage
        policy to.
                :type assigned_to: CreateStoragePolicyAssignmentAssignedTo
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'storage_policy': storage_policy,
            'assigned_to': assigned_to,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/storage_policy_assignments',
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
        return deserialize(response.data, StoragePolicyAssignment)

    def get_storage_policy_assignment_by_id(
        self,
        storage_policy_assignment_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> StoragePolicyAssignment:
        """
                Fetches a specific storage policy assignment.
                :param storage_policy_assignment_id: The ID of the storage policy assignment.
        Example: "932483"
                :type storage_policy_assignment_id: str
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
                        '/2.0/storage_policy_assignments/',
                        to_string(storage_policy_assignment_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, StoragePolicyAssignment)

    def update_storage_policy_assignment_by_id(
        self,
        storage_policy_assignment_id: str,
        storage_policy: UpdateStoragePolicyAssignmentByIdStoragePolicy,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> StoragePolicyAssignment:
        """
                Updates a specific storage policy assignment.
                :param storage_policy_assignment_id: The ID of the storage policy assignment.
        Example: "932483"
                :type storage_policy_assignment_id: str
                :param storage_policy: The storage policy to assign to the user or
        enterprise.
                :type storage_policy: UpdateStoragePolicyAssignmentByIdStoragePolicy
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'storage_policy': storage_policy}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/storage_policy_assignments/',
                        to_string(storage_policy_assignment_id),
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
        return deserialize(response.data, StoragePolicyAssignment)

    def delete_storage_policy_assignment_by_id(
        self,
        storage_policy_assignment_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Delete a storage policy assignment.

                Deleting a storage policy assignment on a user


                will have the user inherit the enterprise's default


                storage policy.


                There is a rate limit for calling this endpoint of only


                twice per user in a 24 hour time frame.

                :param storage_policy_assignment_id: The ID of the storage policy assignment.
        Example: "932483"
                :type storage_policy_assignment_id: str
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
                        '/2.0/storage_policy_assignments/',
                        to_string(storage_policy_assignment_id),
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
