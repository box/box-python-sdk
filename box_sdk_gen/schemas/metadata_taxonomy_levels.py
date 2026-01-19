from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.metadata_taxonomy_level import MetadataTaxonomyLevel

from box_sdk_gen.box.errors import BoxSDKError


class MetadataTaxonomyLevels(BaseObject):
    def __init__(
        self, *, entries: Optional[List[MetadataTaxonomyLevel]] = None, **kwargs
    ):
        """
        :param entries: An array of all taxonomy levels., defaults to None
        :type entries: Optional[List[MetadataTaxonomyLevel]], optional
        """
        super().__init__(**kwargs)
        self.entries = entries
