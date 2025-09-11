from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class MetadataFieldFilterDateRange(BaseObject):
    def __init__(
        self, *, lt: Optional[DateTime] = None, gt: Optional[DateTime] = None, **kwargs
    ):
        """
                :param lt: Specifies the (inclusive) upper bound for the metadata field
        value. The value of a field must be lower than (`lt`) or
        equal to this value for the search query to match this
        template., defaults to None
                :type lt: Optional[DateTime], optional
                :param gt: Specifies the (inclusive) lower bound for the metadata field
        value. The value of a field must be greater than (`gt`) or
        equal to this value for the search query to match this
        template., defaults to None
                :type gt: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.lt = lt
        self.gt = gt
