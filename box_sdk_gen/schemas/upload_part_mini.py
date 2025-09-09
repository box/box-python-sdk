from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class UploadPartMini(BaseObject):
    def __init__(
        self,
        *,
        part_id: Optional[str] = None,
        offset: Optional[int] = None,
        size: Optional[int] = None,
        **kwargs
    ):
        """
                :param part_id: The unique ID of the chunk., defaults to None
                :type part_id: Optional[str], optional
                :param offset: The offset of the chunk within the file
        in bytes. The lower bound of the position
        of the chunk within the file., defaults to None
                :type offset: Optional[int], optional
                :param size: The size of the chunk in bytes., defaults to None
                :type size: Optional[int], optional
        """
        super().__init__(**kwargs)
        self.part_id = part_id
        self.offset = offset
        self.size = size
