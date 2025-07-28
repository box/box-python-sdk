from enum import Enum

from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.user_base import UserBase

from box_sdk_gen.schemas.group_base import GroupBase

from box_sdk_gen.schemas.ai_agent_allowed_entity import AiAgentAllowedEntity

from box_sdk_gen.schemas.ai_studio_agent_ask import AiStudioAgentAsk

from box_sdk_gen.schemas.ai_studio_agent_text_gen import AiStudioAgentTextGen

from box_sdk_gen.schemas.ai_studio_agent_extract import AiStudioAgentExtract

from box_sdk_gen.box.errors import BoxSDKError


class CreateAiAgentTypeField(str, Enum):
    AI_AGENT = 'ai_agent'


class CreateAiAgent(BaseObject):
    _discriminator = 'type', {'ai_agent'}

    def __init__(
        self,
        name: str,
        access_state: str,
        *,
        type: CreateAiAgentTypeField = CreateAiAgentTypeField.AI_AGENT,
        icon_reference: Optional[str] = None,
        allowed_entities: Optional[List[AiAgentAllowedEntity]] = None,
        ask: Optional[AiStudioAgentAsk] = None,
        text_gen: Optional[AiStudioAgentTextGen] = None,
        extract: Optional[AiStudioAgentExtract] = None,
        **kwargs
    ):
        """
                :param name: The name of the AI Agent.
                :type name: str
                :param access_state: The state of the AI Agent. Possible values are: `enabled`, `disabled`, and `enabled_for_selected_users`.
                :type access_state: str
                :param type: The type of agent used to handle queries., defaults to CreateAiAgentTypeField.AI_AGENT
                :type type: CreateAiAgentTypeField, optional
                :param icon_reference: The icon reference of the AI Agent. It should have format of the URL `https://cdn01.boxcdn.net/app-assets/aistudio/avatars/<file_name>`
        where possible values of `file_name` are: `logo_boxAi.png`,`logo_stamp.png`,`logo_legal.png`,`logo_finance.png`,`logo_config.png`,`logo_handshake.png`,`logo_analytics.png`,`logo_classification.png`., defaults to None
                :type icon_reference: Optional[str], optional
                :param allowed_entities: List of allowed users or groups., defaults to None
                :type allowed_entities: Optional[List[AiAgentAllowedEntity]], optional
        """
        super().__init__(**kwargs)
        self.name = name
        self.access_state = access_state
        self.type = type
        self.icon_reference = icon_reference
        self.allowed_entities = allowed_entities
        self.ask = ask
        self.text_gen = text_gen
        self.extract = extract
