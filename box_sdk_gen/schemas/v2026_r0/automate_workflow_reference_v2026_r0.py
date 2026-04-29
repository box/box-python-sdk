from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class AutomateWorkflowReferenceV2026R0TypeField(str, Enum):
    WORKFLOW = 'workflow'


class AutomateWorkflowReferenceV2026R0(BaseObject):
    _discriminator = 'type', {'workflow'}

    def __init__(
        self,
        id: str,
        *,
        type: AutomateWorkflowReferenceV2026R0TypeField = AutomateWorkflowReferenceV2026R0TypeField.WORKFLOW,
        name: Optional[str] = None,
        **kwargs
    ):
        """
        :param id: The identifier for the Automate workflow instance.
        :type id: str
        :param type: The object type., defaults to AutomateWorkflowReferenceV2026R0TypeField.WORKFLOW
        :type type: AutomateWorkflowReferenceV2026R0TypeField, optional
        :param name: The display name for the Automate workflow., defaults to None
        :type name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.name = name
