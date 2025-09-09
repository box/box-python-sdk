from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.file_version_legal_hold import FileVersionLegalHold

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.file_version_legal_holds import FileVersionLegalHolds

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


class FileVersionLegalHoldsManager:
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

    def get_file_version_legal_hold_by_id(
        self,
        file_version_legal_hold_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> FileVersionLegalHold:
        """
                Retrieves information about the legal hold policies

                assigned to a file version.

                :param file_version_legal_hold_id: The ID of the file version legal hold.
        Example: "2348213"
                :type file_version_legal_hold_id: str
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
                        '/2.0/file_version_legal_holds/',
                        to_string(file_version_legal_hold_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, FileVersionLegalHold)

    def get_file_version_legal_holds(
        self,
        policy_id: str,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> FileVersionLegalHolds:
        """
                Get a list of file versions on legal hold for a legal hold

                assignment.


                Due to ongoing re-architecture efforts this API might not return all file


                versions for this policy ID.


                Instead, this API will only return file versions held in the legacy


                architecture. Two new endpoints will available to request any file versions


                held in the new architecture.


                For file versions held in the new architecture, the `GET


                /legal_hold_policy_assignments/:id/file_versions_on_hold` API can be used to


                return all past file versions available for this policy assignment, and the


                `GET /legal_hold_policy_assignments/:id/files_on_hold` API can be used to


                return any current (latest) versions of a file under legal hold.


                The `GET /legal_hold_policy_assignments?policy_id={id}` API can be used to


                find a list of policy assignments for a given policy ID.


                Once the re-architecture is completed this API will be deprecated.

                :param policy_id: The ID of the legal hold policy to get the file version legal
        holds for.
                :type policy_id: str
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
                'policy_id': to_string(policy_id),
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
                        '/2.0/file_version_legal_holds',
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
        return deserialize(response.data, FileVersionLegalHolds)
