from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class AiTaxonomyReferenceTypeField(str, Enum):
    TAXONOMY = 'taxonomy'


class AiTaxonomyReference(BaseObject):
    _discriminator = 'type', {'taxonomy'}

    def __init__(
        self,
        *,
        type: Optional[AiTaxonomyReferenceTypeField] = None,
        taxonomy_key: Optional[str] = None,
        namespace: Optional[str] = None,
        **kwargs
    ):
        """
        :param type: The type of the taxonomy source., defaults to None
        :type type: Optional[AiTaxonomyReferenceTypeField], optional
        :param taxonomy_key: The identifier for a taxonomy, which corresponds to the `taxonomy_key` of the taxonomy source., defaults to None
        :type taxonomy_key: Optional[str], optional
        :param namespace: The namespace of the taxonomy source., defaults to None
        :type namespace: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.taxonomy_key = taxonomy_key
        self.namespace = namespace
