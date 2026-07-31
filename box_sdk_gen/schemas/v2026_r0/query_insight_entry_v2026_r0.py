from enum import Enum

from typing import List

from typing import Dict

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.query_insight_metric_result_v2026_r0 import (
    QueryInsightMetricResultV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class QueryInsightEntryV2026R0TypeField(str, Enum):
    GROUP = 'group'
    OVERALL = 'overall'
    OTHER = 'other'


class QueryInsightEntryV2026R0(BaseObject):
    _discriminator = 'type', {'group', 'overall', 'other'}

    def __init__(
        self,
        key: List[str],
        type: QueryInsightEntryV2026R0TypeField,
        metrics: Dict[str, QueryInsightMetricResultV2026R0],
        **kwargs
    ):
        """
                :param key: The grouping key values associated with the entry. Contains one value per
        `group_by` field for `group` entries, and is empty for `overall` and
        `other` entries.
                :type key: List[str]
                :param type: The type of insight entry, indicating how the associated metrics are
        aggregated.
                :type type: QueryInsightEntryV2026R0TypeField
                :param metrics: A map of metric aliases to their computed results. For `other` entries, the
        count is reported under the `totalCountBeyondTopGroups` key.
                :type metrics: Dict[str, QueryInsightMetricResultV2026R0]
        """
        super().__init__(**kwargs)
        self.key = key
        self.type = type
        self.metrics = metrics
