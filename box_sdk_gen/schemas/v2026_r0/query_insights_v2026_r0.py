from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.query_insight_entry_v2026_r0 import (
    QueryInsightEntryV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class QueryInsightsV2026R0(BaseObject):
    def __init__(self, insights: List[QueryInsightEntryV2026R0], **kwargs):
        """
                :param insights: The list of computed insight entries. Each entry corresponds to a group,
        the overall dataset, or the aggregate of groups outside the top results.
                :type insights: List[QueryInsightEntryV2026R0]
        """
        super().__init__(**kwargs)
        self.insights = insights
