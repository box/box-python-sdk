from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.schemas.retention_policy_mini import RetentionPolicyMini

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class RetentionPolicyAssignmentTypeField(str, Enum):
    RETENTION_POLICY_ASSIGNMENT = 'retention_policy_assignment'


class RetentionPolicyAssignmentAssignedToTypeField(str, Enum):
    FOLDER = 'folder'
    ENTERPRISE = 'enterprise'
    METADATA_TEMPLATE = 'metadata_template'


class RetentionPolicyAssignmentAssignedToField(BaseObject):
    _discriminator = 'type', {'folder', 'enterprise', 'metadata_template'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[RetentionPolicyAssignmentAssignedToTypeField] = None,
        **kwargs
    ):
        """
                :param id: The ID of the folder, enterprise, or metadata template
        the policy is assigned to.
        Set to null or omit when type is set to enterprise., defaults to None
                :type id: Optional[str], optional
                :param type: The type of resource the policy is assigned to., defaults to None
                :type type: Optional[RetentionPolicyAssignmentAssignedToTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class RetentionPolicyAssignmentFilterFieldsField(BaseObject):
    def __init__(
        self, *, field: Optional[str] = None, value: Optional[str] = None, **kwargs
    ):
        """
                :param field: The metadata attribute key id., defaults to None
                :type field: Optional[str], optional
                :param value: The metadata attribute field id. For value, only
        enum and multiselect types are supported., defaults to None
                :type value: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.field = field
        self.value = value


class RetentionPolicyAssignment(BaseObject):
    _discriminator = 'type', {'retention_policy_assignment'}

    def __init__(
        self,
        id: str,
        *,
        type: RetentionPolicyAssignmentTypeField = RetentionPolicyAssignmentTypeField.RETENTION_POLICY_ASSIGNMENT,
        retention_policy: Optional[RetentionPolicyMini] = None,
        assigned_to: Optional[RetentionPolicyAssignmentAssignedToField] = None,
        filter_fields: Optional[
            List[RetentionPolicyAssignmentFilterFieldsField]
        ] = None,
        assigned_by: Optional[UserMini] = None,
        assigned_at: Optional[DateTime] = None,
        start_date_field: Optional[str] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for a retention policy assignment.
                :type id: str
                :param type: The value will always be `retention_policy_assignment`., defaults to RetentionPolicyAssignmentTypeField.RETENTION_POLICY_ASSIGNMENT
                :type type: RetentionPolicyAssignmentTypeField, optional
                :param assigned_to: The `type` and `id` of the content that is under
        retention. The `type` can either be `folder`
        `enterprise`, or `metadata_template`., defaults to None
                :type assigned_to: Optional[RetentionPolicyAssignmentAssignedToField], optional
                :param filter_fields: An array of field objects. Values are only returned if the `assigned_to`
        type is `metadata_template`. Otherwise, the array is blank., defaults to None
                :type filter_fields: Optional[List[RetentionPolicyAssignmentFilterFieldsField]], optional
                :param assigned_at: When the retention policy assignment object was
        created., defaults to None
                :type assigned_at: Optional[DateTime], optional
                :param start_date_field: The date the retention policy assignment begins.
        If the `assigned_to` type is `metadata_template`,
        this field can be a date field's metadata attribute key id., defaults to None
                :type start_date_field: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.retention_policy = retention_policy
        self.assigned_to = assigned_to
        self.filter_fields = filter_fields
        self.assigned_by = assigned_by
        self.assigned_at = assigned_at
        self.start_date_field = start_date_field
