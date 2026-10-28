from typing import List

from box_sdk_gen.schemas.v2026_r0.document_failures_v2026_r0 import (
    DocumentFailuresV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class DocumentSplitFailuresV2026R0(DocumentFailuresV2026R0):
    def __init__(self, errors: List[str], warnings: List[str], **kwargs):
        """
        :param errors: A list of errors that occurred during the document job.
        :type errors: List[str]
        :param warnings: A list of warnings that occurred during the document job.
        :type warnings: List[str]
        """
        super().__init__(errors=errors, warnings=warnings, **kwargs)
