from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.schemas.workflow_mini import WorkflowMiniTypeField

from box_sdk_gen.schemas.workflow_mini import WorkflowMini

from box_sdk_gen.schemas.user_base import UserBase

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class WorkflowFlowsTypeField(str, Enum):
    FLOW = 'flow'


class WorkflowFlowsTriggerTypeField(str, Enum):
    TRIGGER = 'trigger'


class WorkflowFlowsTriggerTriggerTypeField(str, Enum):
    WORKFLOW_MANUAL_START = 'WORKFLOW_MANUAL_START'


class WorkflowFlowsTriggerScopeTypeField(str, Enum):
    TRIGGER_SCOPE = 'trigger_scope'


class WorkflowFlowsTriggerScopeObjectTypeField(str, Enum):
    FOLDER = 'folder'


class WorkflowFlowsTriggerScopeObjectField(BaseObject):
    _discriminator = 'type', {'folder'}

    def __init__(
        self,
        *,
        type: Optional[WorkflowFlowsTriggerScopeObjectTypeField] = None,
        id: Optional[str] = None,
        **kwargs
    ):
        """
        :param type: The type of the object., defaults to None
        :type type: Optional[WorkflowFlowsTriggerScopeObjectTypeField], optional
        :param id: The id of the object., defaults to None
        :type id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id


class WorkflowFlowsTriggerScopeField(BaseObject):
    _discriminator = 'type', {'trigger_scope'}

    def __init__(
        self,
        *,
        type: Optional[WorkflowFlowsTriggerScopeTypeField] = None,
        ref: Optional[str] = None,
        object: Optional[WorkflowFlowsTriggerScopeObjectField] = None,
        **kwargs
    ):
        """
        :param type: The trigger scope's resource type., defaults to None
        :type type: Optional[WorkflowFlowsTriggerScopeTypeField], optional
        :param ref: Indicates the path of the condition value to check., defaults to None
        :type ref: Optional[str], optional
        :param object: The object the `ref` points to., defaults to None
        :type object: Optional[WorkflowFlowsTriggerScopeObjectField], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.ref = ref
        self.object = object


class WorkflowFlowsTriggerField(BaseObject):
    _discriminator = 'type', {'trigger'}

    def __init__(
        self,
        *,
        type: Optional[WorkflowFlowsTriggerTypeField] = None,
        trigger_type: Optional[WorkflowFlowsTriggerTriggerTypeField] = None,
        scope: Optional[List[WorkflowFlowsTriggerScopeField]] = None,
        **kwargs
    ):
        """
        :param type: The trigger's resource type., defaults to None
        :type type: Optional[WorkflowFlowsTriggerTypeField], optional
        :param trigger_type: The type of trigger selected for this flow., defaults to None
        :type trigger_type: Optional[WorkflowFlowsTriggerTriggerTypeField], optional
        :param scope: List of trigger scopes., defaults to None
        :type scope: Optional[List[WorkflowFlowsTriggerScopeField]], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.trigger_type = trigger_type
        self.scope = scope


class WorkflowFlowsOutcomesTypeField(str, Enum):
    OUTCOME = 'outcome'


class WorkflowFlowsOutcomesActionTypeField(str, Enum):
    ADD_METADATA = 'add_metadata'
    ASSIGN_TASK = 'assign_task'
    COPY_FILE = 'copy_file'
    COPY_FOLDER = 'copy_folder'
    CREATE_FOLDER = 'create_folder'
    DELETE_FILE = 'delete_file'
    DELETE_FOLDER = 'delete_folder'
    LOCK_FILE = 'lock_file'
    MOVE_FILE = 'move_file'
    MOVE_FOLDER = 'move_folder'
    REMOVE_WATERMARK_FILE = 'remove_watermark_file'
    RENAME_FOLDER = 'rename_folder'
    RESTORE_FOLDER = 'restore_folder'
    SHARE_FILE = 'share_file'
    SHARE_FOLDER = 'share_folder'
    UNLOCK_FILE = 'unlock_file'
    UPLOAD_FILE = 'upload_file'
    WAIT_FOR_TASK = 'wait_for_task'
    WATERMARK_FILE = 'watermark_file'
    GO_BACK_TO_STEP = 'go_back_to_step'
    APPLY_FILE_CLASSIFICATION = 'apply_file_classification'
    APPLY_FOLDER_CLASSIFICATION = 'apply_folder_classification'
    SEND_NOTIFICATION = 'send_notification'


class WorkflowFlowsOutcomesIfRejectedTypeField(str, Enum):
    OUTCOME = 'outcome'


class WorkflowFlowsOutcomesIfRejectedActionTypeField(str, Enum):
    ADD_METADATA = 'add_metadata'
    ASSIGN_TASK = 'assign_task'
    COPY_FILE = 'copy_file'
    COPY_FOLDER = 'copy_folder'
    CREATE_FOLDER = 'create_folder'
    DELETE_FILE = 'delete_file'
    DELETE_FOLDER = 'delete_folder'
    LOCK_FILE = 'lock_file'
    MOVE_FILE = 'move_file'
    MOVE_FOLDER = 'move_folder'
    REMOVE_WATERMARK_FILE = 'remove_watermark_file'
    RENAME_FOLDER = 'rename_folder'
    RESTORE_FOLDER = 'restore_folder'
    SHARE_FILE = 'share_file'
    SHARE_FOLDER = 'share_folder'
    UNLOCK_FILE = 'unlock_file'
    UPLOAD_FILE = 'upload_file'
    WAIT_FOR_TASK = 'wait_for_task'
    WATERMARK_FILE = 'watermark_file'
    GO_BACK_TO_STEP = 'go_back_to_step'
    APPLY_FILE_CLASSIFICATION = 'apply_file_classification'
    APPLY_FOLDER_CLASSIFICATION = 'apply_folder_classification'
    SEND_NOTIFICATION = 'send_notification'


class WorkflowFlowsOutcomesIfRejectedField(BaseObject):
    _discriminator = 'type', {'outcome'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[WorkflowFlowsOutcomesIfRejectedTypeField] = None,
        name: Optional[str] = None,
        action_type: Optional[WorkflowFlowsOutcomesIfRejectedActionTypeField] = None,
        **kwargs
    ):
        """
        :param id: The identifier of the outcome., defaults to None
        :type id: Optional[str], optional
        :param type: The outcomes resource type., defaults to None
        :type type: Optional[WorkflowFlowsOutcomesIfRejectedTypeField], optional
        :param name: The name of the outcome., defaults to None
        :type name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.name = name
        self.action_type = action_type


class WorkflowFlowsOutcomesField(BaseObject):
    _discriminator = 'type', {'outcome'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[WorkflowFlowsOutcomesTypeField] = None,
        name: Optional[str] = None,
        action_type: Optional[WorkflowFlowsOutcomesActionTypeField] = None,
        if_rejected: Optional[List[WorkflowFlowsOutcomesIfRejectedField]] = None,
        **kwargs
    ):
        """
                :param id: The identifier of the outcome., defaults to None
                :type id: Optional[str], optional
                :param type: The outcomes resource type., defaults to None
                :type type: Optional[WorkflowFlowsOutcomesTypeField], optional
                :param name: The name of the outcome., defaults to None
                :type name: Optional[str], optional
                :param if_rejected: If `action_type` is `assign_task` and the task is rejected, returns a
        list of outcomes to complete., defaults to None
                :type if_rejected: Optional[List[WorkflowFlowsOutcomesIfRejectedField]], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.name = name
        self.action_type = action_type
        self.if_rejected = if_rejected


class WorkflowFlowsField(BaseObject):
    _discriminator = 'type', {'flow'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[WorkflowFlowsTypeField] = None,
        trigger: Optional[WorkflowFlowsTriggerField] = None,
        outcomes: Optional[List[WorkflowFlowsOutcomesField]] = None,
        created_at: Optional[DateTime] = None,
        created_by: Optional[UserBase] = None,
        **kwargs
    ):
        """
        :param id: The identifier of the flow., defaults to None
        :type id: Optional[str], optional
        :param type: The flow's resource type., defaults to None
        :type type: Optional[WorkflowFlowsTypeField], optional
        :param created_at: When this flow was created., defaults to None
        :type created_at: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.trigger = trigger
        self.outcomes = outcomes
        self.created_at = created_at
        self.created_by = created_by


class Workflow(WorkflowMini):
    def __init__(
        self,
        *,
        flows: Optional[List[WorkflowFlowsField]] = None,
        id: Optional[str] = None,
        type: Optional[WorkflowMiniTypeField] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        is_enabled: Optional[bool] = None,
        **kwargs
    ):
        """
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
            id=id,
            type=type,
            name=name,
            description=description,
            is_enabled=is_enabled,
            **kwargs
        )
        self.flows = flows
