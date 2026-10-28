from enum import Enum

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleMappingErrorV2026R0TypeField(str, Enum):
    SHUTTLE_MAPPING_ERROR = 'shuttle_mapping_error'


class ShuttleMappingErrorV2026R0(BaseObject):
    _discriminator = 'type', {'shuttle_mapping_error'}

    def __init__(
        self,
        id: str,
        job_id: str,
        revision: int,
        category: str,
        path: str,
        messages: List[str],
        *,
        type: ShuttleMappingErrorV2026R0TypeField = ShuttleMappingErrorV2026R0TypeField.SHUTTLE_MAPPING_ERROR,
        **kwargs
    ):
        """
                :param id: The unique identifier for the mapping error.
                :type id: str
                :param job_id: The unique identifier of the shuttle job this error belongs to.
                :type job_id: str
                :param revision: The mapping revision this error belongs to.
                :type revision: int
                :param category: The category of mapping work that produced the error. This is an open
        string whose set of values can grow.
                :type category: str
                :param path: The path or subject that the mapping error refers to.
                :type path: str
                :param messages: Human-readable messages describing the mapping error.
                :type messages: List[str]
                :param type: The value will always be `shuttle_mapping_error`., defaults to ShuttleMappingErrorV2026R0TypeField.SHUTTLE_MAPPING_ERROR
                :type type: ShuttleMappingErrorV2026R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.job_id = job_id
        self.revision = revision
        self.category = category
        self.path = path
        self.messages = messages
        self.type = type
