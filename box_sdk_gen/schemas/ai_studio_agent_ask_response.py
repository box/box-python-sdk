from enum import Enum

from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.ai_studio_agent_long_text_tool_response import (
    AiStudioAgentLongTextToolResponse,
)

from box_sdk_gen.schemas.ai_studio_agent_basic_text_tool_response import (
    AiStudioAgentBasicTextToolResponse,
)

from box_sdk_gen.schemas.ai_studio_agent_spreadsheet_tool_response import (
    AiStudioAgentSpreadsheetToolResponse,
)

from box_sdk_gen.box.errors import BoxSDKError


class AiStudioAgentAskResponseTypeField(str, Enum):
    AI_AGENT_ASK = 'ai_agent_ask'


class AiStudioAgentAskResponse(BaseObject):
    _discriminator = 'type', {'ai_agent_ask'}

    def __init__(
        self,
        access_state: str,
        description: str,
        *,
        type: AiStudioAgentAskResponseTypeField = AiStudioAgentAskResponseTypeField.AI_AGENT_ASK,
        custom_instructions: Optional[str] = None,
        suggested_questions: Optional[List[str]] = None,
        long_text: Optional[AiStudioAgentLongTextToolResponse] = None,
        basic_text: Optional[AiStudioAgentBasicTextToolResponse] = None,
        basic_image: Optional[AiStudioAgentBasicTextToolResponse] = None,
        spreadsheet: Optional[AiStudioAgentSpreadsheetToolResponse] = None,
        long_text_multi: Optional[AiStudioAgentLongTextToolResponse] = None,
        basic_text_multi: Optional[AiStudioAgentBasicTextToolResponse] = None,
        basic_image_multi: Optional[AiStudioAgentBasicTextToolResponse] = None,
        **kwargs
    ):
        """
        :param access_state: The state of the AI Agent capability. Possible values are: `enabled` and `disabled`.
        :type access_state: str
        :param description: The description of the AI agent.
        :type description: str
        :param type: The type of AI agent used to ask questions., defaults to AiStudioAgentAskResponseTypeField.AI_AGENT_ASK
        :type type: AiStudioAgentAskResponseTypeField, optional
        :param custom_instructions: Custom instructions for the AI agent., defaults to None
        :type custom_instructions: Optional[str], optional
        :param suggested_questions: Suggested questions for the AI agent. If null, suggested question will be generated. If empty, no suggested questions will be displayed., defaults to None
        :type suggested_questions: Optional[List[str]], optional
        """
        super().__init__(**kwargs)
        self.access_state = access_state
        self.description = description
        self.type = type
        self.custom_instructions = custom_instructions
        self.suggested_questions = suggested_questions
        self.long_text = long_text
        self.basic_text = basic_text
        self.basic_image = basic_image
        self.spreadsheet = spreadsheet
        self.long_text_multi = long_text_multi
        self.basic_text_multi = basic_text_multi
        self.basic_image_multi = basic_image_multi
