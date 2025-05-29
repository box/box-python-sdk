from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.ai_studio_agent_basic_gen_tool_response import AiStudioAgentBasicGenToolResponse

from box_sdk_gen.box.errors import BoxSDKError

class AiStudioAgentTextGenResponseTypeField(str, Enum):
    AI_AGENT_TEXT_GEN = 'ai_agent_text_gen'

class AiStudioAgentTextGenResponse(BaseObject):
    _discriminator = 'type', {'ai_agent_text_gen'}
    def __init__(self, access_state: str, description: str, *, type: AiStudioAgentTextGenResponseTypeField = AiStudioAgentTextGenResponseTypeField.AI_AGENT_TEXT_GEN, custom_instructions: Optional[str] = None, basic_gen: Optional[AiStudioAgentBasicGenToolResponse] = None, **kwargs):
        """
        :param access_state: The state of the AI Agent capability. Possible values are: `enabled` and `disabled`.
        :type access_state: str
        :param description: The description of the AI Agent.
        :type description: str
        :param type: The type of AI agent used for generating text., defaults to AiStudioAgentTextGenResponseTypeField.AI_AGENT_TEXT_GEN
        :type type: AiStudioAgentTextGenResponseTypeField, optional
        :param custom_instructions: Custom instructions for the agent., defaults to None
        :type custom_instructions: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.access_state = access_state
        self.description = description
        self.type = type
        self.custom_instructions = custom_instructions
        self.basic_gen = basic_gen