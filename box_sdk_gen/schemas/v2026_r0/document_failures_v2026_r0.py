from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class DocumentFailuresV2026R0(BaseObject):
    def __init__(self, errors: List[str], warnings: List[str], **kwargs):
        """
        :param errors: A list of errors that occurred during the document job.
        :type errors: List[str]
        :param warnings: A list of warnings that occurred during the document job.
        :type warnings: List[str]
        """
        super().__init__(**kwargs)
        self.errors = errors
        self.warnings = warnings
