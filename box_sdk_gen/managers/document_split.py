from enum import Enum

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.schemas.v2026_r0.document_split_create_request_manual_v2026_r0 import (
    DocumentSplitCreateRequestManualV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.document_split_create_request_page_selection_v2026_r0 import (
    DocumentSplitCreateRequestPageSelectionV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.document_split_create_request_smart_v2026_r0 import (
    DocumentSplitCreateRequestSmartV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.document_split_create_request_type_v2026_r0 import (
    DocumentSplitCreateRequestTypeV2026R0,
)

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.v2026_r0.document_split_create_response_v2026_r0 import (
    DocumentSplitCreateResponseV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.client_error_v2026_r0 import ClientErrorV2026R0

from box_sdk_gen.parameters.v2026_r0.box_version_header_v2026_r0 import (
    BoxVersionHeaderV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.document_split_create_request_v2026_r0 import (
    DocumentSplitCreateRequestV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.document_splits_v2026_r0 import DocumentSplitsV2026R0

from box_sdk_gen.schemas.v2026_r0.document_split_v2026_r0 import DocumentSplitV2026R0

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


class CreateDocumentSplitV2026R0InputSource(str, Enum):
    API = 'api'
    BOX = 'box'
    RELAY = 'relay'
    SALESFORCE = 'salesforce'


class DocumentSplitManager:
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

    def create_document_split_v2026_r0(
        self,
        source_file_id: str,
        destination_folder_id: str,
        input_source: CreateDocumentSplitV2026R0InputSource,
        split_input: DocumentSplitCreateRequestTypeV2026R0,
        *,
        external_id: Optional[str] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> DocumentSplitCreateResponseV2026R0:
        """
                Initiates a Document Split job for the supplied source file. The job runs

                asynchronously; clients can poll the returned job ID to track progress.


                All split-specific input lives under `split_input`. When


                `split_input.split_type` is `manual`, provide


                `split_input.split_definition` (continuous page ranges; `version` may be


                omitted or `v_1`). When `split_input.split_type` is `page_selection`,


                provide `split_input.page_selection` (non-linear page segments; `version`


                may be omitted or `v_2`). `split_input.prompt` must not be provided for


                either of those variants. When `split_input.split_type` is `smart`,


                `split_input.prompt` is required and neither


                `split_input.split_definition` nor `split_input.page_selection` must be


                provided.

                :param source_file_id: The ID of the source file to split.
                :type source_file_id: str
                :param destination_folder_id: The ID of the folder where the resulting files will be uploaded.
                :type destination_folder_id: str
                :param input_source: The system that initiated the request, used for analytics and
        traceability.
                :type input_source: CreateDocumentSplitV2026R0InputSource
                :param external_id: An optional identifier supplied by the caller for this Document Split job.
        The value is returned on job responses for correlation only. It is not
        a Box resource ID, is not required to be unique, and cannot be used to
        look up the job., defaults to None
                :type external_id: Optional[str], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'source_file_id': source_file_id,
            'destination_folder_id': destination_folder_id,
            'input_source': input_source,
            'split_input': split_input,
            'external_id': external_id,
        }
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/document_splits']
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
        return deserialize(response.data, DocumentSplitCreateResponseV2026R0)

    def get_document_splits_v2026_r0(
        self,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> DocumentSplitsV2026R0:
        """
                Returns a paginated list of Document Split jobs accessible to the

                authenticated user.

                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {'marker': to_string(marker), 'limit': to_string(limit)}
        )
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/document_splits']
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, DocumentSplitsV2026R0)

    def get_document_split_by_id_v2026_r0(
        self,
        document_split_id: str,
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> DocumentSplitV2026R0:
        """
                Returns details for a single Document Split job identified by its ID,

                including the current status, the input definition, and any output files


                produced by the job.

                :param document_split_id: The unique identifier for the Document Split job.
        Example: "1748426"
                :type document_split_id: str
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
                        '/2.0/document_splits/',
                        to_string(document_split_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, DocumentSplitV2026R0)
