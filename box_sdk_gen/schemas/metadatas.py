from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.metadata import Metadata

from box_sdk_gen.box.errors import BoxSDKError


class Metadatas(BaseObject):
    def __init__(
        self,
        *,
        entries: Optional[List[Metadata]] = None,
        limit: Optional[int] = None,
        **kwargs
    ):
        """
        :param entries: A list of metadata instances, as applied to this file or folder., defaults to None
        :type entries: Optional[List[Metadata]], optional
        :param limit: The limit that was used for this page of results., defaults to None
        :type limit: Optional[int], optional
        """
        super().__init__(**kwargs)
        self.entries = entries
        self.limit = limit
