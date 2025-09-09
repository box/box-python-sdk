from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.ai_agent_long_text_tool import AiAgentLongTextTool

from box_sdk_gen.schemas.ai_agent_basic_text_tool import AiAgentBasicTextTool

from box_sdk_gen.box.errors import BoxSDKError


class AiAgentExtractTypeField(str, Enum):
    AI_AGENT_EXTRACT = 'ai_agent_extract'


class AiAgentExtract(BaseObject):
    _discriminator = 'type', {'ai_agent_extract'}

    def __init__(
        self,
        *,
        type: AiAgentExtractTypeField = AiAgentExtractTypeField.AI_AGENT_EXTRACT,
        long_text: Optional[AiAgentLongTextTool] = None,
        basic_text: Optional[AiAgentBasicTextTool] = None,
        basic_image: Optional[AiAgentBasicTextTool] = None,
        **kwargs
    ):
        """
        :param type: The type of AI agent to be used for extraction., defaults to AiAgentExtractTypeField.AI_AGENT_EXTRACT
        :type type: AiAgentExtractTypeField, optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.long_text = long_text
        self.basic_text = basic_text
        self.basic_image = basic_image
