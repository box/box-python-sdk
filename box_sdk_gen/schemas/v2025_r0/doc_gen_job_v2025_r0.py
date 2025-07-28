from enum import Enum

from typing import Optional

from box_sdk_gen.schemas.v2025_r0.doc_gen_job_base_v2025_r0 import (
    DocGenJobBaseV2025R0TypeField,
)

from box_sdk_gen.schemas.v2025_r0.doc_gen_job_base_v2025_r0 import DocGenJobBaseV2025R0

from box_sdk_gen.schemas.v2025_r0.doc_gen_batch_base_v2025_r0 import (
    DocGenBatchBaseV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.file_reference_v2025_r0 import FileReferenceV2025R0

from box_sdk_gen.schemas.v2025_r0.file_version_base_v2025_r0 import (
    FileVersionBaseV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class DocGenJobV2025R0StatusField(str, Enum):
    SUBMITTED = 'submitted'
    COMPLETED = 'completed'
    FAILED = 'failed'
    COMPLETED_WITH_ERROR = 'completed_with_error'
    PENDING = 'pending'


class DocGenJobV2025R0(DocGenJobBaseV2025R0):
    def __init__(
        self,
        batch: DocGenBatchBaseV2025R0,
        template_file: FileReferenceV2025R0,
        template_file_version: FileVersionBaseV2025R0,
        status: DocGenJobV2025R0StatusField,
        output_type: str,
        id: str,
        *,
        output_file: Optional[Optional[FileReferenceV2025R0]] = None,
        output_file_version: Optional[Optional[FileVersionBaseV2025R0]] = None,
        type: DocGenJobBaseV2025R0TypeField = DocGenJobBaseV2025R0TypeField.DOCGEN_JOB,
        **kwargs
    ):
        """
        :param status: Status of the job.
        :type status: DocGenJobV2025R0StatusField
        :param output_type: Type of the generated file.
        :type output_type: str
        :param id: The unique identifier that represent a Box Doc Gen job.
        :type id: str
        :param type: The value will always be `docgen_job`., defaults to DocGenJobBaseV2025R0TypeField.DOCGEN_JOB
        :type type: DocGenJobBaseV2025R0TypeField, optional
        """
        super().__init__(id=id, type=type, **kwargs)
        self.batch = batch
        self.template_file = template_file
        self.template_file_version = template_file_version
        self.status = status
        self.output_type = output_type
        self.output_file = output_file
        self.output_file_version = output_file_version
