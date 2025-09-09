from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class DocGenJobBaseV2025R0TypeField(str, Enum):
    DOCGEN_JOB = 'docgen_job'


class DocGenJobBaseV2025R0(BaseObject):
    _discriminator = 'type', {'docgen_job'}

    def __init__(
        self,
        id: str,
        *,
        type: DocGenJobBaseV2025R0TypeField = DocGenJobBaseV2025R0TypeField.DOCGEN_JOB,
        **kwargs
    ):
        """
        :param id: The unique identifier that represent a Box Doc Gen job.
        :type id: str
        :param type: The value will always be `docgen_job`., defaults to DocGenJobBaseV2025R0TypeField.DOCGEN_JOB
        :type type: DocGenJobBaseV2025R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
