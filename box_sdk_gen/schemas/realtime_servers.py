from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.realtime_server import RealtimeServer

from box_sdk_gen.box.errors import BoxSDKError


class RealtimeServers(BaseObject):
    def __init__(
        self,
        *,
        chunk_size: Optional[int] = None,
        entries: Optional[List[RealtimeServer]] = None,
        **kwargs
    ):
        """
        :param chunk_size: The number of items in this response., defaults to None
        :type chunk_size: Optional[int], optional
        :param entries: A list of real-time servers., defaults to None
        :type entries: Optional[List[RealtimeServer]], optional
        """
        super().__init__(**kwargs)
        self.chunk_size = chunk_size
        self.entries = entries
