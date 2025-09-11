from typing import Union

from box_sdk_gen.schemas.ai_agent_reference import AiAgentReference

from box_sdk_gen.schemas.ai_agent_text_gen import AiAgentTextGen

from box_sdk_gen.box.errors import BoxSDKError

AiTextGenAgent = Union[AiAgentReference, AiAgentTextGen]
