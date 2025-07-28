from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class DocGenBatchBaseV2025R0TypeField(str, Enum):
    DOCGEN_BATCH = 'docgen_batch'


class DocGenBatchBaseV2025R0(BaseObject):
    _discriminator = 'type', {'docgen_batch'}

    def __init__(
        self,
        id: str,
        *,
        type: DocGenBatchBaseV2025R0TypeField = DocGenBatchBaseV2025R0TypeField.DOCGEN_BATCH,
        **kwargs
    ):
        """
        :param id: The unique identifier that represents a Box Doc Gen batch.
        :type id: str
        :param type: The value will always be `docgen_batch`., defaults to DocGenBatchBaseV2025R0TypeField.DOCGEN_BATCH
        :type type: DocGenBatchBaseV2025R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
