from typing import Dict

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.ai_agent_info import AiAgentInfo

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class AiExtractStructuredResponse(BaseObject):
    def __init__(
        self,
        answer: Dict,
        created_at: DateTime,
        *,
        completion_reason: Optional[str] = None,
        confidence_score: Optional[Dict] = None,
        ai_agent_info: Optional[AiAgentInfo] = None,
        **kwargs
    ):
        """
        :param created_at: The ISO date formatted timestamp of when the answer to the prompt was created.
        :type created_at: DateTime
        :param completion_reason: The reason the response finishes., defaults to None
        :type completion_reason: Optional[str], optional
        :param confidence_score: The confidence score numeric values for each extracted field as a JSON dictionary. This can be empty if no field could be extracted., defaults to None
        :type confidence_score: Optional[Dict], optional
        """
        super().__init__(**kwargs)
        self.answer = answer
        self.created_at = created_at
        self.completion_reason = completion_reason
        self.confidence_score = confidence_score
        self.ai_agent_info = ai_agent_info
