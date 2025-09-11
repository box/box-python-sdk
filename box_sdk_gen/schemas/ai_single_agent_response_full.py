from typing import Optional

from typing import List

from box_sdk_gen.schemas.ai_single_agent_response import AiSingleAgentResponseTypeField

from box_sdk_gen.schemas.user_base import UserBase

from box_sdk_gen.internal.utils import DateTime

from box_sdk_gen.schemas.group_base import GroupBase

from box_sdk_gen.schemas.ai_agent_allowed_entity import AiAgentAllowedEntity

from box_sdk_gen.schemas.ai_single_agent_response import AiSingleAgentResponse

from box_sdk_gen.schemas.ai_studio_agent_ask_response import AiStudioAgentAskResponse

from box_sdk_gen.schemas.ai_studio_agent_text_gen_response import (
    AiStudioAgentTextGenResponse,
)

from box_sdk_gen.schemas.ai_studio_agent_extract_response import (
    AiStudioAgentExtractResponse,
)

from box_sdk_gen.box.errors import BoxSDKError


class AiSingleAgentResponseFull(AiSingleAgentResponse):
    def __init__(
        self,
        id: str,
        origin: str,
        name: str,
        access_state: str,
        *,
        ask: Optional[AiStudioAgentAskResponse] = None,
        text_gen: Optional[AiStudioAgentTextGenResponse] = None,
        extract: Optional[AiStudioAgentExtractResponse] = None,
        type: Optional[AiSingleAgentResponseTypeField] = None,
        created_by: Optional[UserBase] = None,
        created_at: Optional[DateTime] = None,
        modified_by: Optional[UserBase] = None,
        modified_at: Optional[DateTime] = None,
        icon_reference: Optional[str] = None,
        allowed_entities: Optional[List[AiAgentAllowedEntity]] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier of the AI Agent.
        :type id: str
        :param origin: The provider of the AI Agent.
        :type origin: str
        :param name: The name of the AI Agent.
        :type name: str
        :param access_state: The state of the AI Agent. Possible values are: `enabled`, `disabled`, and `enabled_for_selected_users`.
        :type access_state: str
        :param type: The type of agent used to handle queries., defaults to None
        :type type: Optional[AiSingleAgentResponseTypeField], optional
        :param created_by: The user who created this agent., defaults to None
        :type created_by: Optional[UserBase], optional
        :param created_at: The ISO date-time formatted timestamp of when this AI agent was created., defaults to None
        :type created_at: Optional[DateTime], optional
        :param modified_by: The user who most recently modified this agent., defaults to None
        :type modified_by: Optional[UserBase], optional
        :param modified_at: The ISO date-time formatted timestamp of when this AI agent was recently modified., defaults to None
        :type modified_at: Optional[DateTime], optional
        :param icon_reference: The icon reference of the AI Agent., defaults to None
        :type icon_reference: Optional[str], optional
        :param allowed_entities: List of allowed users or groups., defaults to None
        :type allowed_entities: Optional[List[AiAgentAllowedEntity]], optional
        """
        super().__init__(
            id=id,
            origin=origin,
            name=name,
            access_state=access_state,
            type=type,
            created_by=created_by,
            created_at=created_at,
            modified_by=modified_by,
            modified_at=modified_at,
            icon_reference=icon_reference,
            allowed_entities=allowed_entities,
            **kwargs
        )
        self.ask = ask
        self.text_gen = text_gen
        self.extract = extract
