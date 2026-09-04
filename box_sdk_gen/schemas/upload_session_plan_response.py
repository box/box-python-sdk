from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.upload_part_plan_hit import UploadPartPlanHit

from box_sdk_gen.schemas.upload_part_plan import UploadPartPlan

from box_sdk_gen.box.errors import BoxSDKError


class UploadSessionPlanResponse(BaseObject):
    def __init__(
        self,
        upload_session_id: str,
        hits: List[UploadPartPlanHit],
        misses: List[UploadPartPlan],
        **kwargs
    ):
        """
                :param upload_session_id: The unique identifier for this upload session.
                :type upload_session_id: str
                :param hits: Parts that already exist on the server and
        do not need to be uploaded again.
                :type hits: List[UploadPartPlanHit]
                :param misses: Parts that do not exist on the server and
        need to be uploaded.
                :type misses: List[UploadPartPlan]
        """
        super().__init__(**kwargs)
        self.upload_session_id = upload_session_id
        self.hits = hits
        self.misses = misses
