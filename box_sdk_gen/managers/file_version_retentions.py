from enum import Enum

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.file_version_retentions import FileVersionRetentions

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.file_version_retention import FileVersionRetention

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


class GetFileVersionRetentionsDispositionAction(str, Enum):
    PERMANENTLY_DELETE = 'permanently_delete'
    REMOVE_RETENTION = 'remove_retention'


class FileVersionRetentionsManager:
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

    def get_file_version_retentions(
        self,
        *,
        file_id: Optional[str] = None,
        file_version_id: Optional[str] = None,
        policy_id: Optional[str] = None,
        disposition_action: Optional[GetFileVersionRetentionsDispositionAction] = None,
        disposition_before: Optional[str] = None,
        disposition_after: Optional[str] = None,
        limit: Optional[int] = None,
        marker: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> FileVersionRetentions:
        """
                Retrieves all file version retentions for the given enterprise.

                **Note**:


                File retention API is now **deprecated**.


                To get information about files and file versions under retention,


                see [files under retention](e://get-retention-policy-assignments-id-files-under-retention) or [file versions under retention](e://get-retention-policy-assignments-id-file-versions-under-retention) endpoints.

                :param file_id: Filters results by files with this ID., defaults to None
                :type file_id: Optional[str], optional
                :param file_version_id: Filters results by file versions with this ID., defaults to None
                :type file_version_id: Optional[str], optional
                :param policy_id: Filters results by the retention policy with this ID., defaults to None
                :type policy_id: Optional[str], optional
                :param disposition_action: Filters results by the retention policy with this disposition
        action., defaults to None
                :type disposition_action: Optional[GetFileVersionRetentionsDispositionAction], optional
                :param disposition_before: Filters results by files that will have their disposition
        come into effect before this date., defaults to None
                :type disposition_before: Optional[str], optional
                :param disposition_after: Filters results by files that will have their disposition
        come into effect after this date., defaults to None
                :type disposition_after: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
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
                'file_id': to_string(file_id),
                'file_version_id': to_string(file_version_id),
                'policy_id': to_string(policy_id),
                'disposition_action': to_string(disposition_action),
                'disposition_before': to_string(disposition_before),
                'disposition_after': to_string(disposition_after),
                'limit': to_string(limit),
                'marker': to_string(marker),
            }
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/file_version_retentions',
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
        return deserialize(response.data, FileVersionRetentions)

    def get_file_version_retention_by_id(
        self,
        file_version_retention_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> FileVersionRetention:
        """
                Returns information about a file version retention.

                **Note**:


                File retention API is now **deprecated**.


                To get information about files and file versions under retention,


                see [files under retention](e://get-retention-policy-assignments-id-files-under-retention) or [file versions under retention](e://get-retention-policy-assignments-id-file-versions-under-retention) endpoints.

                :param file_version_retention_id: The ID of the file version retention.
        Example: "3424234"
                :type file_version_retention_id: str
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
                        '/2.0/file_version_retentions/',
                        to_string(file_version_retention_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, FileVersionRetention)
