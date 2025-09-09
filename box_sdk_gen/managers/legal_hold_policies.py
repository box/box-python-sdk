from typing import Optional

from typing import List

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.legal_hold_policies import LegalHoldPolicies

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.legal_hold_policy import LegalHoldPolicy

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

from box_sdk_gen.internal.utils import DateTime


class LegalHoldPoliciesManager:
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

    def get_legal_hold_policies(
        self,
        *,
        policy_name: Optional[str] = None,
        fields: Optional[List[str]] = None,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> LegalHoldPolicies:
        """
                Retrieves a list of legal hold policies that belong to

                an enterprise.

                :param policy_name: Limits results to policies for which the names start with
        this search term. This is a case-insensitive prefix., defaults to None
                :type policy_name: Optional[str], optional
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
                'policy_name': to_string(policy_name),
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
                        '/2.0/legal_hold_policies',
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
        return deserialize(response.data, LegalHoldPolicies)

    def create_legal_hold_policy(
        self,
        policy_name: str,
        *,
        description: Optional[str] = None,
        filter_started_at: Optional[DateTime] = None,
        filter_ended_at: Optional[DateTime] = None,
        is_ongoing: Optional[bool] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> LegalHoldPolicy:
        """
                Create a new legal hold policy.
                :param policy_name: The name of the policy.
                :type policy_name: str
                :param description: A description for the policy., defaults to None
                :type description: Optional[str], optional
                :param filter_started_at: The filter start date.

        When this policy is applied using a `custodian` legal
        hold assignments, it will only apply to file versions
        created or uploaded inside of the
        date range. Other assignment types, such as folders and
        files, will ignore the date filter.

        Required if `is_ongoing` is set to `false`., defaults to None
                :type filter_started_at: Optional[DateTime], optional
                :param filter_ended_at: The filter end date.

        When this policy is applied using a `custodian` legal
        hold assignments, it will only apply to file versions
        created or uploaded inside of the
        date range. Other assignment types, such as folders and
        files, will ignore the date filter.

        Required if `is_ongoing` is set to `false`., defaults to None
                :type filter_ended_at: Optional[DateTime], optional
                :param is_ongoing: Whether new assignments under this policy should
        continue applying to files even after initialization.

        When this policy is applied using a legal hold assignment,
        it will continue applying the policy to any new file versions
        even after it has been applied.

        For example, if a legal hold assignment is placed on a user
        today, and that user uploads a file tomorrow, that file will
        get held. This will continue until the policy is retired.

        Required if no filter dates are set., defaults to None
                :type is_ongoing: Optional[bool], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'policy_name': policy_name,
            'description': description,
            'filter_started_at': filter_started_at,
            'filter_ended_at': filter_ended_at,
            'is_ongoing': is_ongoing,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/legal_hold_policies',
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
        return deserialize(response.data, LegalHoldPolicy)

    def get_legal_hold_policy_by_id(
        self,
        legal_hold_policy_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> LegalHoldPolicy:
        """
                Retrieve a legal hold policy.
                :param legal_hold_policy_id: The ID of the legal hold policy.
        Example: "324432"
                :type legal_hold_policy_id: str
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
                        '/2.0/legal_hold_policies/',
                        to_string(legal_hold_policy_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, LegalHoldPolicy)

    def update_legal_hold_policy_by_id(
        self,
        legal_hold_policy_id: str,
        *,
        policy_name: Optional[str] = None,
        description: Optional[str] = None,
        release_notes: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> LegalHoldPolicy:
        """
                Update legal hold policy.
                :param legal_hold_policy_id: The ID of the legal hold policy.
        Example: "324432"
                :type legal_hold_policy_id: str
                :param policy_name: The name of the policy., defaults to None
                :type policy_name: Optional[str], optional
                :param description: A description for the policy., defaults to None
                :type description: Optional[str], optional
                :param release_notes: Notes around why the policy was released., defaults to None
                :type release_notes: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'policy_name': policy_name,
            'description': description,
            'release_notes': release_notes,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/legal_hold_policies/',
                        to_string(legal_hold_policy_id),
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
        return deserialize(response.data, LegalHoldPolicy)

    def delete_legal_hold_policy_by_id(
        self,
        legal_hold_policy_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Delete an existing legal hold policy.

                This is an asynchronous process. The policy will not be


                fully deleted yet when the response returns.

                :param legal_hold_policy_id: The ID of the legal hold policy.
        Example: "324432"
                :type legal_hold_policy_id: str
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
                        '/2.0/legal_hold_policies/',
                        to_string(legal_hold_policy_id),
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
