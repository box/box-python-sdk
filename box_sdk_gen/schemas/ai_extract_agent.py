from typing import Union

from box_sdk_gen.schemas.ai_agent_reference import AiAgentReference

from box_sdk_gen.schemas.ai_agent_extract import AiAgentExtract

from box_sdk_gen.box.errors import BoxSDKError

AiExtractAgent = Union[AiAgentReference, AiAgentExtract]
