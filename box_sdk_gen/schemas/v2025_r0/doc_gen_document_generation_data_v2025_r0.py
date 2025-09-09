from typing import Dict

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class DocGenDocumentGenerationDataV2025R0(BaseObject):
    def __init__(self, generated_file_name: str, user_input: Dict, **kwargs):
        """
        :param generated_file_name: File name of the output file.
        :type generated_file_name: str
        """
        super().__init__(**kwargs)
        self.generated_file_name = generated_file_name
        self.user_input = user_input
