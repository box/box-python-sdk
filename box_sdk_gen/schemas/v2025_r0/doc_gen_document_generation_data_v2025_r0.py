from typing import Dict

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class DocGenDocumentGenerationDataV2025R0(BaseObject):
    def __init__(
        self,
        generated_file_name: str,
        user_input: Dict,
        *,
        external_id: Optional[str] = None,
        **kwargs
    ):
        """
                :param generated_file_name: File name of the output file.
                :type generated_file_name: str
                :param external_id: An optional identifier supplied by the caller for this Box Doc Gen job.
        The value is returned on job responses for correlation only. It is not
        a Box resource ID, is not required to be unique, and cannot be used to
        look up the job., defaults to None
                :type external_id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.generated_file_name = generated_file_name
        self.user_input = user_input
        self.external_id = external_id
