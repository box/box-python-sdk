from typing import Optional

from typing import Union

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.event import Event

from box_sdk_gen.box.errors import BoxSDKError


class Events(BaseObject):
    def __init__(
        self,
        *,
        chunk_size: Optional[int] = None,
        next_stream_position: Optional[Union[str, int]] = None,
        entries: Optional[List[Event]] = None,
        **kwargs
    ):
        """
                :param chunk_size: The number of events returned in this response., defaults to None
                :type chunk_size: Optional[int], optional
                :param next_stream_position: The stream position of the start of the next page (chunk)
        of events., defaults to None
                :type next_stream_position: Optional[Union[str, int]], optional
                :param entries: A list of events., defaults to None
                :type entries: Optional[List[Event]], optional
        """
        super().__init__(**kwargs)
        self.chunk_size = chunk_size
        self.next_stream_position = next_stream_position
        self.entries = entries
