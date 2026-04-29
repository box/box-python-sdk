from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.user_mini_v2026_r0 import UserMiniV2026R0

from box_sdk_gen.schemas.v2026_r0.automate_workflow_reference_v2026_r0 import (
    AutomateWorkflowReferenceV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class AutomateWorkflowActionV2026R0TypeField(str, Enum):
    WORKFLOW_ACTION = 'workflow_action'


class AutomateWorkflowActionV2026R0ActionTypeField(str, Enum):
    RUN_WORKFLOW = 'run_workflow'


class AutomateWorkflowActionV2026R0(BaseObject):
    _discriminator = 'type', {'workflow_action'}

    def __init__(
        self,
        id: str,
        workflow: AutomateWorkflowReferenceV2026R0,
        *,
        type: AutomateWorkflowActionV2026R0TypeField = AutomateWorkflowActionV2026R0TypeField.WORKFLOW_ACTION,
        action_type: AutomateWorkflowActionV2026R0ActionTypeField = AutomateWorkflowActionV2026R0ActionTypeField.RUN_WORKFLOW,
        description: Optional[str] = None,
        created_at: Optional[DateTime] = None,
        updated_at: Optional[DateTime] = None,
        created_by: Optional[UserMiniV2026R0] = None,
        updated_by: Optional[UserMiniV2026R0] = None,
        **kwargs
    ):
        """
        :param id: The identifier for the Automate action.
        :type id: str
        :param type: The object type for this workflow action wrapper., defaults to AutomateWorkflowActionV2026R0TypeField.WORKFLOW_ACTION
        :type type: AutomateWorkflowActionV2026R0TypeField, optional
        :param action_type: The type that defines the behavior of this action., defaults to AutomateWorkflowActionV2026R0ActionTypeField.RUN_WORKFLOW
        :type action_type: AutomateWorkflowActionV2026R0ActionTypeField, optional
        :param description: A human-readable description of the workflow action., defaults to None
        :type description: Optional[str], optional
        :param created_at: The date and time when the action was created., defaults to None
        :type created_at: Optional[DateTime], optional
        :param updated_at: The date and time when the action was last updated., defaults to None
        :type updated_at: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.workflow = workflow
        self.type = type
        self.action_type = action_type
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        self.created_by = created_by
        self.updated_by = updated_by
