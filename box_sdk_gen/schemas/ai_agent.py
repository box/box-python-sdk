from typing import Union

from box_sdk_gen.schemas.ai_agent_ask import AiAgentAsk

from box_sdk_gen.schemas.ai_agent_text_gen import AiAgentTextGen

from box_sdk_gen.schemas.ai_agent_extract import AiAgentExtract

from box_sdk_gen.schemas.ai_agent_extract_structured import AiAgentExtractStructured

from box_sdk_gen.box.errors import BoxSDKError

AiAgent = Union[AiAgentAsk, AiAgentTextGen, AiAgentExtract, AiAgentExtractStructured]
