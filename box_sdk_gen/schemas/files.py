from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.box.errors import BoxSDKError


class Files(BaseObject):
    def __init__(
        self,
        *,
        total_count: Optional[int] = None,
        entries: Optional[List[FileFull]] = None,
        **kwargs
    ):
        """
        :param total_count: The number of files., defaults to None
        :type total_count: Optional[int], optional
        :param entries: A list of files., defaults to None
        :type entries: Optional[List[FileFull]], optional
        """
        super().__init__(**kwargs)
        self.total_count = total_count
        self.entries = entries
