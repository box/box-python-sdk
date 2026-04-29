from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class AutomateWorkflowStartRequestV2026R0(BaseObject):
    def __init__(self, workflow_action_id: str, file_ids: List[str], **kwargs):
        """
        :param workflow_action_id: The callable action ID used to trigger the selected workflow.
        :type workflow_action_id: str
        :param file_ids: The files to process with the selected workflow.
        :type file_ids: List[str]
        """
        super().__init__(**kwargs)
        self.workflow_action_id = workflow_action_id
        self.file_ids = file_ids
