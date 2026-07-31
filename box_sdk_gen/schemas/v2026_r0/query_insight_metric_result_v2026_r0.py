from typing import Dict

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class QueryInsightMetricResultV2026R0(BaseObject):
    def __init__(self, type: str, values: Dict[str, float], **kwargs):
        """
                :param type: The metric type that was computed.
                :type type: str
                :param values: The computed metric result(s), keyed by the metric function (for example
        `sum`, `avg`, `min`, `max`, or `count`).
                :type values: Dict[str, float]
        """
        super().__init__(**kwargs)
        self.type = type
        self.values = values
