from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.ai_studio_agent_long_text_tool_response import (
    AiStudioAgentLongTextToolResponse,
)

from box_sdk_gen.schemas.ai_studio_agent_basic_text_tool_response import (
    AiStudioAgentBasicTextToolResponse,
)

from box_sdk_gen.box.errors import BoxSDKError


class AiStudioAgentExtractResponseTypeField(str, Enum):
    AI_AGENT_EXTRACT = 'ai_agent_extract'


class AiStudioAgentExtractResponse(BaseObject):
    _discriminator = 'type', {'ai_agent_extract'}

    def __init__(
        self,
        access_state: str,
        description: str,
        *,
        type: AiStudioAgentExtractResponseTypeField = AiStudioAgentExtractResponseTypeField.AI_AGENT_EXTRACT,
        custom_instructions: Optional[str] = None,
        long_text: Optional[AiStudioAgentLongTextToolResponse] = None,
        basic_text: Optional[AiStudioAgentBasicTextToolResponse] = None,
        basic_image: Optional[AiStudioAgentBasicTextToolResponse] = None,
        **kwargs
    ):
        """
        :param access_state: The state of the AI Agent capability. Possible values are: `enabled` and `disabled`.
        :type access_state: str
        :param description: The description of the AI agent.
        :type description: str
        :param type: The type of AI agent to be used for metadata extraction., defaults to AiStudioAgentExtractResponseTypeField.AI_AGENT_EXTRACT
        :type type: AiStudioAgentExtractResponseTypeField, optional
        :param custom_instructions: Custom instructions for the AI agent., defaults to None
        :type custom_instructions: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.access_state = access_state
        self.description = description
        self.type = type
        self.custom_instructions = custom_instructions
        self.long_text = long_text
        self.basic_text = basic_text
        self.basic_image = basic_image
