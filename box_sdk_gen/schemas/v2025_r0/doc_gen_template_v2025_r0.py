from typing import Optional

from box_sdk_gen.schemas.v2025_r0.file_reference_v2025_r0 import FileReferenceV2025R0

from box_sdk_gen.schemas.v2025_r0.doc_gen_template_base_v2025_r0 import (
    DocGenTemplateBaseV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class DocGenTemplateV2025R0(DocGenTemplateBaseV2025R0):
    def __init__(
        self,
        *,
        file_name: Optional[str] = None,
        file: Optional[FileReferenceV2025R0] = None,
        **kwargs
    ):
        """
        :param file_name: The name of the template., defaults to None
        :type file_name: Optional[str], optional
        """
        super().__init__(file=file, **kwargs)
        self.file_name = file_name
