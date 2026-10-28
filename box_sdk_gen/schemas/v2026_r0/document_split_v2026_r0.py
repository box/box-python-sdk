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

from box_sdk_gen.schemas.v2026_r0.file_reference_v2026_r0 import FileReferenceV2026R0

from box_sdk_gen.schemas.v2026_r0.document_split_create_request_type_v2026_r0 import (
    DocumentSplitCreateRequestTypeV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.document_split_output_v2026_r0 import (
    DocumentSplitOutputV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.folder_reference_v2026_r0 import (
    FolderReferenceV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.user_mini_v2026_r0 import UserMiniV2026R0

from box_sdk_gen.schemas.v2026_r0.enterprise_reference_v2026_r0 import (
    EnterpriseReferenceV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.document_split_failures_v2026_r0 import (
    DocumentSplitFailuresV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class DocumentSplitV2026R0TypeField(str, Enum):
    DOCUMENT_SPLIT = 'document_split'


class DocumentSplitV2026R0StatusField(str, Enum):
    SUBMITTED = 'submitted'
    COMPLETED = 'completed'
    FAILED = 'failed'
    COMPLETED_WITH_ERROR = 'completed_with_error'


class DocumentSplitV2026R0InputSourceField(str, Enum):
    API = 'api'
    BOX = 'box'
    RELAY = 'relay'
    SALESFORCE = 'salesforce'


class DocumentSplitV2026R0(BaseObject):
    _discriminator = 'type', {'document_split'}

    def __init__(
        self,
        id: str,
        source_file: FileReferenceV2026R0,
        status: DocumentSplitV2026R0StatusField,
        split_input: DocumentSplitCreateRequestTypeV2026R0,
        destination_folder: FolderReferenceV2026R0,
        input_source: DocumentSplitV2026R0InputSourceField,
        *,
        type: DocumentSplitV2026R0TypeField = DocumentSplitV2026R0TypeField.DOCUMENT_SPLIT,
        output: Optional[DocumentSplitOutputV2026R0] = None,
        created_at: Optional[DateTime] = None,
        created_by: Optional[UserMiniV2026R0] = None,
        enterprise: Optional[EnterpriseReferenceV2026R0] = None,
        failures: Optional[DocumentSplitFailuresV2026R0] = None,
        external_id: Optional[str] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for the Document Split job.
                :type id: str
                :param status: The current state of the Document Split job.
                :type status: DocumentSplitV2026R0StatusField
                :param input_source: The system that initiated the request, used for analytics and
        traceability.
                :type input_source: DocumentSplitV2026R0InputSourceField
                :param type: The value will always be `document_split`., defaults to DocumentSplitV2026R0TypeField.DOCUMENT_SPLIT
                :type type: DocumentSplitV2026R0TypeField, optional
                :param output: The result of the Document Split job. `null` until the job has produced
        output., defaults to None
                :type output: Optional[DocumentSplitOutputV2026R0], optional
                :param created_at: When the Document Split job was created., defaults to None
                :type created_at: Optional[DateTime], optional
                :param failures: Errors and warnings that occurred during the document split. `null` when
        no failures were recorded., defaults to None
                :type failures: Optional[DocumentSplitFailuresV2026R0], optional
                :param external_id: An optional identifier supplied by the caller when the Document Split
        job was created. Returned for correlation only. It is not a Box
        resource ID, is not required to be unique, and cannot be used to
        look up the job., defaults to None
                :type external_id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.source_file = source_file
        self.status = status
        self.split_input = split_input
        self.destination_folder = destination_folder
        self.input_source = input_source
        self.type = type
        self.output = output
        self.created_at = created_at
        self.created_by = created_by
        self.enterprise = enterprise
        self.failures = failures
        self.external_id = external_id
