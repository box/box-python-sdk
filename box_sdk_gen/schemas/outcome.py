from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.collaborator_variable import CollaboratorVariable

from box_sdk_gen.schemas.completion_rule_variable import CompletionRuleVariable

from box_sdk_gen.schemas.role_variable import RoleVariable

from box_sdk_gen.box.errors import BoxSDKError


class Outcome(BaseObject):
    def __init__(
        self,
        id: str,
        *,
        collaborators: Optional[CollaboratorVariable] = None,
        completion_rule: Optional[CompletionRuleVariable] = None,
        file_collaborator_role: Optional[RoleVariable] = None,
        task_collaborators: Optional[CollaboratorVariable] = None,
        role: Optional[RoleVariable] = None,
        **kwargs
    ):
        """
        :param id: ID of a specific outcome.
        :type id: str
        """
        super().__init__(**kwargs)
        self.id = id
        self.collaborators = collaborators
        self.completion_rule = completion_rule
        self.file_collaborator_role = file_collaborator_role
        self.task_collaborators = task_collaborators
        self.role = role
