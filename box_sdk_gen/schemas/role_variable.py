from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class RoleVariableTypeField(str, Enum):
    VARIABLE = 'variable'


class RoleVariableVariableTypeField(str, Enum):
    COLLABORATOR_ROLE = 'collaborator_role'


class RoleVariableVariableValueField(str, Enum):
    EDITOR = 'editor'
    VIEWER = 'viewer'
    PREVIEWER = 'previewer'
    UPLOADER = 'uploader'
    PREVIEWER_UPLOADER = 'previewer uploader'
    VIEWER_UPLOADER = 'viewer uploader'
    CO_OWNER = 'co-owner'


class RoleVariable(BaseObject):
    _discriminator = 'type', {'variable'}

    def __init__(
        self,
        variable_value: RoleVariableVariableValueField,
        *,
        type: RoleVariableTypeField = RoleVariableTypeField.VARIABLE,
        variable_type: RoleVariableVariableTypeField = RoleVariableVariableTypeField.COLLABORATOR_ROLE,
        **kwargs
    ):
        """
                :param type: Role object type., defaults to RoleVariableTypeField.VARIABLE
                :type type: RoleVariableTypeField, optional
                :param variable_type: The variable type used
        by the object., defaults to RoleVariableVariableTypeField.COLLABORATOR_ROLE
                :type variable_type: RoleVariableVariableTypeField, optional
        """
        super().__init__(**kwargs)
        self.variable_value = variable_value
        self.type = type
        self.variable_type = variable_type
