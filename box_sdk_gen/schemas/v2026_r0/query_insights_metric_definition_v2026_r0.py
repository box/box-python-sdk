from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class QueryInsightsMetricDefinitionV2026R0TypeField(str, Enum):
    SUM = 'sum'
    AVG = 'avg'
    MIN = 'min'
    MAX = 'max'
    COUNT = 'count'


class QueryInsightsMetricDefinitionV2026R0(BaseObject):
    _discriminator = 'type', {'sum', 'avg', 'min', 'max', 'count'}

    def __init__(
        self, type: QueryInsightsMetricDefinitionV2026R0TypeField, field: str, **kwargs
    ):
        """
        :param type: The aggregation function to apply.
        :type type: QueryInsightsMetricDefinitionV2026R0TypeField
        :param field: The fully qualified field name on which the metric is computed.
        :type field: str
        """
        super().__init__(**kwargs)
        self.type = type
        self.field = field
