from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from typing import Optional

from typing import List

from box_sdk_gen.schemas.v2025_r0.file_reference_v2025_r0 import FileReferenceV2025R0

from box_sdk_gen.schemas.v2025_r0.file_version_base_v2025_r0 import (
    FileVersionBaseV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.doc_gen_document_generation_data_v2025_r0 import (
    DocGenDocumentGenerationDataV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class DocGenBatchCreateRequestV2025R0DestinationFolderTypeField(str, Enum):
    FOLDER = 'folder'


class DocGenBatchCreateRequestV2025R0DestinationFolderField(BaseObject):
    _discriminator = 'type', {'folder'}

    def __init__(
        self,
        id: str,
        *,
        type: DocGenBatchCreateRequestV2025R0DestinationFolderTypeField = DocGenBatchCreateRequestV2025R0DestinationFolderTypeField.FOLDER,
        **kwargs
    ):
        """
        :param id: ID of the folder.
        :type id: str
        :param type: The value will always be `folder`., defaults to DocGenBatchCreateRequestV2025R0DestinationFolderTypeField.FOLDER
        :type type: DocGenBatchCreateRequestV2025R0DestinationFolderTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class DocGenBatchCreateRequestV2025R0(BaseObject):
    def __init__(
        self,
        file: FileReferenceV2025R0,
        input_source: str,
        destination_folder: DocGenBatchCreateRequestV2025R0DestinationFolderField,
        output_type: str,
        document_generation_data: List[DocGenDocumentGenerationDataV2025R0],
        *,
        file_version: Optional[FileVersionBaseV2025R0] = None,
        **kwargs
    ):
        """
        :param input_source: Source of input. The value has to be `api` for all the API-based document generation requests.
        :type input_source: str
        :param output_type: Type of the output file.
        :type output_type: str
        """
        super().__init__(**kwargs)
        self.file = file
        self.input_source = input_source
        self.destination_folder = destination_folder
        self.output_type = output_type
        self.document_generation_data = document_generation_data
        self.file_version = file_version
