from typing import Union

from box_sdk_gen.schemas.ai_agent_reference import AiAgentReference

from box_sdk_gen.schemas.ai_agent_extract_structured import AiAgentExtractStructured

from box_sdk_gen.box.errors import BoxSDKError

AiExtractStructuredAgent = Union[AiAgentReference, AiAgentExtractStructured]
