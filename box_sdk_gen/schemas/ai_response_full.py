from typing import Optional

from typing import List

from box_sdk_gen.internal.utils import DateTime

from box_sdk_gen.schemas.ai_agent_info import AiAgentInfo

from box_sdk_gen.schemas.ai_response import AiResponse

from box_sdk_gen.schemas.ai_citation import AiCitation

from box_sdk_gen.box.errors import BoxSDKError


class AiResponseFull(AiResponse):
    def __init__(
        self,
        answer: str,
        created_at: DateTime,
        *,
        citations: Optional[List[AiCitation]] = None,
        completion_reason: Optional[str] = None,
        ai_agent_info: Optional[AiAgentInfo] = None,
        **kwargs
    ):
        """
        :param answer: The answer provided by the LLM.
        :type answer: str
        :param created_at: The ISO date formatted timestamp of when the answer to the prompt was created.
        :type created_at: DateTime
        :param citations: The citations of the LLM's answer reference., defaults to None
        :type citations: Optional[List[AiCitation]], optional
        :param completion_reason: The reason the response finishes., defaults to None
        :type completion_reason: Optional[str], optional
        """
        super().__init__(
            answer=answer,
            created_at=created_at,
            completion_reason=completion_reason,
            ai_agent_info=ai_agent_info,
            **kwargs
        )
        self.citations = citations
