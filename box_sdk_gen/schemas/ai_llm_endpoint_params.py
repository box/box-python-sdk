from typing import Union

from box_sdk_gen.schemas.ai_llm_endpoint_params_open_ai import AiLlmEndpointParamsOpenAi

from box_sdk_gen.schemas.ai_llm_endpoint_params_google import AiLlmEndpointParamsGoogle

from box_sdk_gen.schemas.ai_llm_endpoint_params_aws import AiLlmEndpointParamsAws

from box_sdk_gen.schemas.ai_llm_endpoint_params_ibm import AiLlmEndpointParamsIbm

from box_sdk_gen.box.errors import BoxSDKError

AiLlmEndpointParams = Union[
    AiLlmEndpointParamsOpenAi,
    AiLlmEndpointParamsGoogle,
    AiLlmEndpointParamsAws,
    AiLlmEndpointParamsIbm,
]
