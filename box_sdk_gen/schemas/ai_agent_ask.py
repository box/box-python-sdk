from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.ai_agent_long_text_tool import AiAgentLongTextTool

from box_sdk_gen.schemas.ai_agent_basic_text_tool import AiAgentBasicTextTool

from box_sdk_gen.schemas.ai_agent_spreadsheet_tool import AiAgentSpreadsheetTool

from box_sdk_gen.box.errors import BoxSDKError


class AiAgentAskTypeField(str, Enum):
    AI_AGENT_ASK = 'ai_agent_ask'


class AiAgentAsk(BaseObject):
    _discriminator = 'type', {'ai_agent_ask'}

    def __init__(
        self,
        *,
        type: AiAgentAskTypeField = AiAgentAskTypeField.AI_AGENT_ASK,
        long_text: Optional[AiAgentLongTextTool] = None,
        basic_text: Optional[AiAgentBasicTextTool] = None,
        spreadsheet: Optional[AiAgentSpreadsheetTool] = None,
        long_text_multi: Optional[AiAgentLongTextTool] = None,
        basic_text_multi: Optional[AiAgentBasicTextTool] = None,
        basic_image: Optional[AiAgentBasicTextTool] = None,
        basic_image_multi: Optional[AiAgentBasicTextTool] = None,
        **kwargs
    ):
        """
        :param type: The type of AI agent used to handle queries., defaults to AiAgentAskTypeField.AI_AGENT_ASK
        :type type: AiAgentAskTypeField, optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.long_text = long_text
        self.basic_text = basic_text
        self.spreadsheet = spreadsheet
        self.long_text_multi = long_text_multi
        self.basic_text_multi = basic_text_multi
        self.basic_image = basic_image
        self.basic_image_multi = basic_image_multi
