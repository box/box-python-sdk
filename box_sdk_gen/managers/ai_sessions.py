from enum import Enum

from typing import Optional

from typing import List

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.v2026_r0.ai_sessions_v2026_r0 import AiSessionsV2026R0

from box_sdk_gen.schemas.v2026_r0.client_error_v2026_r0 import ClientErrorV2026R0

from box_sdk_gen.parameters.v2026_r0.box_version_header_v2026_r0 import (
    BoxVersionHeaderV2026R0,
)

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


class GetAiSessionsV2026R0Source(str, Enum):
    API = 'api'


class GetAiSessionsV2026R0Sort(str, Enum):
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'
    NAME = 'name'


class GetAiSessionsV2026R0Direction(str, Enum):
    ASC = 'asc'
    DESC = 'desc'


class AiSessionsManager:
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

    def get_ai_sessions_v2026_r0(
        self,
        source: GetAiSessionsV2026R0Source,
        *,
        marker: Optional[str] = None,
        sort: Optional[GetAiSessionsV2026R0Sort] = None,
        direction: Optional[GetAiSessionsV2026R0Direction] = None,
        limit: Optional[int] = None,
        client_ids: Optional[List[str]] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> AiSessionsV2026R0:
        """
                Returns a marker-paginated list of the AI sessions that the authenticated

                user can read and that were created through the Box public API. Entries are


                ordered by `sort` and `direction`, defaulting to `updated_at` descending so


                the most recently active session appears first.


                The access token must have both the `ai.readwrite` and `root_readwrite`


                scopes.


                A page may contain fewer than `limit` entries while further pages remain.


                Treat a non-null `next_marker` as the only signal that more results exist.

                :param source: Restricts the list to AI sessions with this origin. The only supported
        value is `api`.
                :type source: GetAiSessionsV2026R0Source
                :param marker: The position marker at which to begin returning results, as returned in
        `next_marker` by the previous page. Omit it for the first page. All other
        parameters must match the request that returned the marker., defaults to None
                :type marker: Optional[str], optional
                :param sort: The field to sort results by. Possible values are `created_at`,
        `updated_at`, and `name`. Default is `updated_at`, which advances on each
        turn of session activity., defaults to None
                :type sort: Optional[GetAiSessionsV2026R0Sort], optional
                :param direction: The direction to sort results in, either ascending (`asc`) or
        descending (`desc`). Default is `desc`., defaults to None
                :type direction: Optional[GetAiSessionsV2026R0Direction], optional
                :param limit: The maximum number of AI sessions to return per page. The maximum is
        `100`; larger values are treated as `100`. The server may return fewer
        entries than requested., defaults to None
                :type limit: Optional[int], optional
                :param client_ids: A comma-separated list of OAuth client IDs. Restricts the list to AI
        sessions created by any of these applications. Client IDs that match no
        application are ignored, so the response is an empty list if none of them
        match. Empty entries are ignored, and an empty value is treated as if the
        parameter were not provided., defaults to None
                :type client_ids: Optional[List[str]], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'source': to_string(source),
                'marker': to_string(marker),
                'sort': to_string(sort),
                'direction': to_string(direction),
                'limit': to_string(limit),
                'client_ids': to_string(client_ids),
            }
        )
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/ai_sessions']
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, AiSessionsV2026R0)

    def delete_ai_session_by_id_v2026_r0(
        self,
        ai_session_id: str,
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Deletes an AI session created through the Box public API, together with its

                agent tasks. The session's agent-generated files and uploaded files are


                moved to the trash. Files attached as sources from elsewhere in Box are not


                affected. Deleting a session does not stop a running task or notify the


                agent.


                The access token must have both the `ai.readwrite` and `root_readwrite`


                scopes.

                :param ai_session_id: The unique identifier of the AI session. This is the same value returned as
        `id` by the list endpoint and used as the A2A `contextId`.
        Example: "23489723"
                :type ai_session_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/ai_sessions/',
                        to_string(ai_session_id),
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
