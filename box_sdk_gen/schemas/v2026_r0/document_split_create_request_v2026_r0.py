from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

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

from box_sdk_gen.box.errors import BoxSDKError


class DocumentSplitCreateRequestV2026R0InputSourceField(str, Enum):
    API = 'api'
    BOX = 'box'
    RELAY = 'relay'
    SALESFORCE = 'salesforce'


class DocumentSplitCreateRequestV2026R0(BaseObject):
    def __init__(
        self,
        source_file_id: str,
        destination_folder_id: str,
        input_source: DocumentSplitCreateRequestV2026R0InputSourceField,
        split_input: DocumentSplitCreateRequestTypeV2026R0,
        *,
        external_id: Optional[str] = None,
        **kwargs
    ):
        """
                :param source_file_id: The ID of the source file to split.
                :type source_file_id: str
                :param destination_folder_id: The ID of the folder where the resulting files will be uploaded.
                :type destination_folder_id: str
                :param input_source: The system that initiated the request, used for analytics and
        traceability.
                :type input_source: DocumentSplitCreateRequestV2026R0InputSourceField
                :param external_id: An optional identifier supplied by the caller for this Document Split job.
        The value is returned on job responses for correlation only. It is not
        a Box resource ID, is not required to be unique, and cannot be used to
        look up the job., defaults to None
                :type external_id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.source_file_id = source_file_id
        self.destination_folder_id = destination_folder_id
        self.input_source = input_source
        self.split_input = split_input
        self.external_id = external_id
