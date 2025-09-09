from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2025_r0.file_reference_v2025_r0 import FileReferenceV2025R0

from box_sdk_gen.box.errors import BoxSDKError


class DocGenTemplateBaseV2025R0(BaseObject):
    def __init__(self, *, file: Optional[FileReferenceV2025R0] = None, **kwargs):
        super().__init__(**kwargs)
        self.file = file
