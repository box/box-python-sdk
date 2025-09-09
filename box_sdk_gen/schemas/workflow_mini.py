from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class WorkflowMiniTypeField(str, Enum):
    WORKFLOW = 'workflow'


class WorkflowMini(BaseObject):
    _discriminator = 'type', {'workflow'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[WorkflowMiniTypeField] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        is_enabled: Optional[bool] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for the workflow., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `workflow`., defaults to None
        :type type: Optional[WorkflowMiniTypeField], optional
        :param name: The name of the workflow., defaults to None
        :type name: Optional[str], optional
        :param description: The description for a workflow., defaults to None
        :type description: Optional[str], optional
        :param is_enabled: Specifies if this workflow is enabled., defaults to None
        :type is_enabled: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.name = name
        self.description = description
        self.is_enabled = is_enabled
