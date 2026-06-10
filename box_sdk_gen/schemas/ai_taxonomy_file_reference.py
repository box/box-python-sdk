from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class AiTaxonomyFileReferenceTypeField(str, Enum):
    FILE = 'file'


class AiTaxonomyFileReference(BaseObject):
    _discriminator = 'type', {'file'}

    def __init__(
        self,
        *,
        type: Optional[AiTaxonomyFileReferenceTypeField] = None,
        taxonomy_key: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs
    ):
        """
        :param type: The type of the taxonomy source., defaults to None
        :type type: Optional[AiTaxonomyFileReferenceTypeField], optional
        :param taxonomy_key: The identifier for a taxonomy, which corresponds to the `taxonomy_key` of the taxonomy source., defaults to None
        :type taxonomy_key: Optional[str], optional
        :param id: The ID of the taxonomy source. Required if the type is `file` and unsupported if the type is `taxonomy`., defaults to None
        :type id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.taxonomy_key = taxonomy_key
        self.id = id
