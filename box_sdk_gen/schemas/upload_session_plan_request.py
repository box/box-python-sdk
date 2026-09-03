from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.upload_part_plan import UploadPartPlan

from box_sdk_gen.box.errors import BoxSDKError


class UploadSessionPlanRequest(BaseObject):
    def __init__(self, parts: List[UploadPartPlan], **kwargs):
        """
        :param parts: The list of parts to check for existence.
        :type parts: List[UploadPartPlan]
        """
        super().__init__(**kwargs)
        self.parts = parts
