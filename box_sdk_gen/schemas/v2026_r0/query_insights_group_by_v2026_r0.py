from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class QueryInsightsGroupByV2026R0(BaseObject):
    def __init__(self, field: str, *, bucket_limit: Optional[int] = None, **kwargs):
        """
                :param field: The fully qualified field name to group by. Supports metadata and item
        properties.
                :type field: str
                :param bucket_limit: The maximum number of buckets to return for the grouping. Defaults to `5`., defaults to None
                :type bucket_limit: Optional[int], optional
        """
        super().__init__(**kwargs)
        self.field = field
        self.bucket_limit = bucket_limit
