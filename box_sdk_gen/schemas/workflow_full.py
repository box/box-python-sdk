from typing import Optional

from typing import List

from box_sdk_gen.schemas.workflow_mini import WorkflowMiniTypeField

from box_sdk_gen.schemas.workflow_mini import WorkflowMini

from box_sdk_gen.schemas.workflow import WorkflowFlowsField

from box_sdk_gen.schemas.workflow import Workflow

from box_sdk_gen.schemas.user_base import UserBase

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class WorkflowFull(Workflow):
    def __init__(
        self,
        *,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        created_by: Optional[UserBase] = None,
        modified_by: Optional[UserBase] = None,
        flows: Optional[List[WorkflowFlowsField]] = None,
        id: Optional[str] = None,
        type: Optional[WorkflowMiniTypeField] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        is_enabled: Optional[bool] = None,
        **kwargs
    ):
        """
        :param created_at: The date and time when the workflow was created on Box., defaults to None
        :type created_at: Optional[DateTime], optional
        :param modified_at: The date and time when the workflow was last updated on Box., defaults to None
        :type modified_at: Optional[DateTime], optional
        :param flows: A list of flows assigned to a workflow., defaults to None
        :type flows: Optional[List[WorkflowFlowsField]], optional
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
        super().__init__(
            flows=flows,
            id=id,
            type=type,
            name=name,
            description=description,
            is_enabled=is_enabled,
            **kwargs
        )
        self.created_at = created_at
        self.modified_at = modified_at
        self.created_by = created_by
        self.modified_by = modified_by
