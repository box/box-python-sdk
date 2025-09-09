from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.box.errors import BoxSDKError


class CollaboratorVariableTypeField(str, Enum):
    VARIABLE = 'variable'


class CollaboratorVariableVariableTypeField(str, Enum):
    USER_LIST = 'user_list'


class CollaboratorVariableVariableValueTypeField(str, Enum):
    USER = 'user'


class CollaboratorVariableVariableValueField(BaseObject):
    _discriminator = 'type', {'user'}

    def __init__(
        self,
        id: str,
        *,
        type: CollaboratorVariableVariableValueTypeField = CollaboratorVariableVariableValueTypeField.USER,
        **kwargs
    ):
        """
        :param id: User's ID.
        :type id: str
        :param type: The object type., defaults to CollaboratorVariableVariableValueTypeField.USER
        :type type: CollaboratorVariableVariableValueTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class CollaboratorVariable(BaseObject):
    _discriminator = 'type', {'variable'}

    def __init__(
        self,
        variable_value: List[CollaboratorVariableVariableValueField],
        *,
        type: CollaboratorVariableTypeField = CollaboratorVariableTypeField.VARIABLE,
        variable_type: CollaboratorVariableVariableTypeField = CollaboratorVariableVariableTypeField.USER_LIST,
        **kwargs
    ):
        """
                :param variable_value: A list of user IDs.
                :type variable_value: List[CollaboratorVariableVariableValueField]
                :param type: Collaborator
        object type., defaults to CollaboratorVariableTypeField.VARIABLE
                :type type: CollaboratorVariableTypeField, optional
                :param variable_type: Variable type
        for the Collaborator
        object., defaults to CollaboratorVariableVariableTypeField.USER_LIST
                :type variable_type: CollaboratorVariableVariableTypeField, optional
        """
        super().__init__(**kwargs)
        self.variable_value = variable_value
        self.type = type
        self.variable_type = variable_type
