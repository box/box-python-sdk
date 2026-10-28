from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class DocumentSplitPageRangeV2026R0(BaseObject):
    def __init__(self, start: int, end: int, **kwargs):
        """
        :param start: The first page (inclusive) included in this slice.
        :type start: int
        :param end: The last page (inclusive) included in this slice.
        :type end: int
        """
        super().__init__(**kwargs)
        self.start = start
        self.end = end
