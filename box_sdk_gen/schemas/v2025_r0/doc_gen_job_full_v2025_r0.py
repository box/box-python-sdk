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

from box_sdk_gen.schemas.v2025_r0.doc_gen_job_v2025_r0 import (
    DocGenJobV2025R0StatusField,
)

from box_sdk_gen.schemas.v2025_r0.doc_gen_job_v2025_r0 import DocGenJobV2025R0

from box_sdk_gen.schemas.v2025_r0.user_base_v2025_r0 import UserBaseV2025R0

from box_sdk_gen.schemas.v2025_r0.enterprise_reference_v2025_r0 import (
    EnterpriseReferenceV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class DocGenJobFullV2025R0(DocGenJobV2025R0):
    def __init__(
        self,
        created_by: UserBaseV2025R0,
        enterprise: EnterpriseReferenceV2025R0,
        source: str,
        batch: DocGenBatchBaseV2025R0,
        template_file: FileReferenceV2025R0,
        template_file_version: FileVersionBaseV2025R0,
        status: DocGenJobV2025R0StatusField,
        output_type: str,
        id: str,
        *,
        created_at: Optional[str] = None,
        output_file: Optional[Optional[FileReferenceV2025R0]] = None,
        output_file_version: Optional[Optional[FileVersionBaseV2025R0]] = None,
        type: DocGenJobBaseV2025R0TypeField = DocGenJobBaseV2025R0TypeField.DOCGEN_JOB,
        **kwargs
    ):
        """
        :param source: Source of the request.
        :type source: str
        :param status: Status of the job.
        :type status: DocGenJobV2025R0StatusField
        :param output_type: Type of the generated file.
        :type output_type: str
        :param id: The unique identifier that represent a Box Doc Gen job.
        :type id: str
        :param created_at: Time of job creation., defaults to None
        :type created_at: Optional[str], optional
        :param type: The value will always be `docgen_job`., defaults to DocGenJobBaseV2025R0TypeField.DOCGEN_JOB
        :type type: DocGenJobBaseV2025R0TypeField, optional
        """
        super().__init__(
            batch=batch,
            template_file=template_file,
            template_file_version=template_file_version,
            status=status,
            output_type=output_type,
            id=id,
            output_file=output_file,
            output_file_version=output_file_version,
            type=type,
            **kwargs
        )
        self.created_by = created_by
        self.enterprise = enterprise
        self.source = source
        self.created_at = created_at
