from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from typing import List

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.v2025_r0.file_reference_v2025_r0 import FileReferenceV2025R0

from box_sdk_gen.schemas.v2025_r0.file_version_base_v2025_r0 import (
    FileVersionBaseV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.doc_gen_document_generation_data_v2025_r0 import (
    DocGenDocumentGenerationDataV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.doc_gen_job_v2025_r0 import DocGenJobV2025R0

from box_sdk_gen.schemas.v2025_r0.client_error_v2025_r0 import ClientErrorV2025R0

from box_sdk_gen.parameters.v2025_r0.box_version_header_v2025_r0 import (
    BoxVersionHeaderV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.doc_gen_jobs_full_v2025_r0 import (
    DocGenJobsFullV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.doc_gen_jobs_v2025_r0 import DocGenJobsV2025R0

from box_sdk_gen.schemas.v2025_r0.doc_gen_batch_base_v2025_r0 import (
    DocGenBatchBaseV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.doc_gen_batch_create_request_v2025_r0 import (
    DocGenBatchCreateRequestV2025R0,
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


class CreateDocgenBatchV2025R0DestinationFolderTypeField(str, Enum):
    FOLDER = 'folder'


class CreateDocgenBatchV2025R0DestinationFolder(BaseObject):
    _discriminator = 'type', {'folder'}

    def __init__(
        self,
        id: str,
        *,
        type: CreateDocgenBatchV2025R0DestinationFolderTypeField = CreateDocgenBatchV2025R0DestinationFolderTypeField.FOLDER,
        **kwargs
    ):
        """
        :param id: ID of the folder.
        :type id: str
        :param type: The value will always be `folder`., defaults to CreateDocgenBatchV2025R0DestinationFolderTypeField.FOLDER
        :type type: CreateDocgenBatchV2025R0DestinationFolderTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class DocgenManager:
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

    def get_docgen_job_by_id_v2025_r0(
        self,
        job_id: str,
        *,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> DocGenJobV2025R0:
        """
                Get details of the Box Doc Gen job.
                :param job_id: Box Doc Gen job ID.
        Example: 123
                :type job_id: str
                :param box_version: Version header., defaults to BoxVersionHeaderV2025R0._2025_0
                :type box_version: BoxVersionHeaderV2025R0, optional
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
                        '/2.0/docgen_jobs/',
                        to_string(job_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, DocGenJobV2025R0)

    def get_docgen_jobs_v2025_r0(
        self,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> DocGenJobsFullV2025R0:
        """
                Lists all Box Doc Gen jobs for a user.
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2025R0._2025_0
                :type box_version: BoxVersionHeaderV2025R0, optional
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
                    [self.network_session.base_urls.base_url, '/2.0/docgen_jobs']
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, DocGenJobsFullV2025R0)

    def get_docgen_batch_job_by_id_v2025_r0(
        self,
        batch_id: str,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> DocGenJobsV2025R0:
        """
                Lists Box Doc Gen jobs in a batch.
                :param batch_id: Box Doc Gen batch ID.
        Example: 123
                :type batch_id: str
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2025R0._2025_0
                :type box_version: BoxVersionHeaderV2025R0, optional
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
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/docgen_batch_jobs/',
                        to_string(batch_id),
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
        return deserialize(response.data, DocGenJobsV2025R0)

    def create_docgen_batch_v2025_r0(
        self,
        file: FileReferenceV2025R0,
        input_source: str,
        destination_folder: CreateDocgenBatchV2025R0DestinationFolder,
        output_type: str,
        document_generation_data: List[DocGenDocumentGenerationDataV2025R0],
        *,
        file_version: Optional[FileVersionBaseV2025R0] = None,
        box_version: BoxVersionHeaderV2025R0 = BoxVersionHeaderV2025R0._2025_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> DocGenBatchBaseV2025R0:
        """
        Generates a document using a Box Doc Gen template.
        :param input_source: Source of input. The value has to be `api` for all the API-based document generation requests.
        :type input_source: str
        :param output_type: Type of the output file.
        :type output_type: str
        :param box_version: Version header., defaults to BoxVersionHeaderV2025R0._2025_0
        :type box_version: BoxVersionHeaderV2025R0, optional
        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'file': file,
            'file_version': file_version,
            'input_source': input_source,
            'destination_folder': destination_folder,
            'output_type': output_type,
            'document_generation_data': document_generation_data,
        }
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/docgen_batches']
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
        return deserialize(response.data, DocGenBatchBaseV2025R0)
