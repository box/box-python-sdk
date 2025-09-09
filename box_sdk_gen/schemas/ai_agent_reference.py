from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class AiAgentReferenceTypeField(str, Enum):
    AI_AGENT_ID = 'ai_agent_id'


class AiAgentReference(BaseObject):
    _discriminator = 'type', {'ai_agent_id'}

    def __init__(
        self,
        *,
        type: AiAgentReferenceTypeField = AiAgentReferenceTypeField.AI_AGENT_ID,
        id: Optional[str] = None,
        **kwargs
    ):
        """
        :param type: The type of AI agent used to handle queries., defaults to AiAgentReferenceTypeField.AI_AGENT_ID
        :type type: AiAgentReferenceTypeField, optional
        :param id: The ID of an Agent., defaults to None
        :type id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id
