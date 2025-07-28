from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.ai_agent_basic_gen_tool import AiAgentBasicGenTool

from box_sdk_gen.box.errors import BoxSDKError


class AiAgentTextGenTypeField(str, Enum):
    AI_AGENT_TEXT_GEN = 'ai_agent_text_gen'


class AiAgentTextGen(BaseObject):
    _discriminator = 'type', {'ai_agent_text_gen'}

    def __init__(
        self,
        *,
        type: AiAgentTextGenTypeField = AiAgentTextGenTypeField.AI_AGENT_TEXT_GEN,
        basic_gen: Optional[AiAgentBasicGenTool] = None,
        **kwargs
    ):
        """
        :param type: The type of AI agent used for generating text., defaults to AiAgentTextGenTypeField.AI_AGENT_TEXT_GEN
        :type type: AiAgentTextGenTypeField, optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.basic_gen = basic_gen
