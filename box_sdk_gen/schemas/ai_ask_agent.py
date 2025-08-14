from typing import Union

from box_sdk_gen.schemas.ai_agent_reference import AiAgentReference

from box_sdk_gen.schemas.ai_agent_ask import AiAgentAsk

from box_sdk_gen.box.errors import BoxSDKError

AiAskAgent = Union[AiAgentReference, AiAgentAsk]
