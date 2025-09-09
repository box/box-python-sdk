from typing import Optional

from box_sdk_gen.schemas.ai_llm_endpoint_params_open_ai import AiLlmEndpointParamsOpenAi

from box_sdk_gen.schemas.ai_llm_endpoint_params_google import AiLlmEndpointParamsGoogle

from box_sdk_gen.schemas.ai_llm_endpoint_params_aws import AiLlmEndpointParamsAws

from box_sdk_gen.schemas.ai_llm_endpoint_params_ibm import AiLlmEndpointParamsIbm

from box_sdk_gen.schemas.ai_llm_endpoint_params import AiLlmEndpointParams

from box_sdk_gen.schemas.ai_agent_spreadsheet_tool import AiAgentSpreadsheetTool

from box_sdk_gen.box.errors import BoxSDKError


class AiStudioAgentSpreadsheetTool(AiAgentSpreadsheetTool):
    def __init__(
        self,
        *,
        model: Optional[str] = None,
        num_tokens_for_completion: Optional[int] = None,
        llm_endpoint_params: Optional[AiLlmEndpointParams] = None,
        **kwargs
    ):
        """
        :param model: The model used for the AI agent for spreadsheets. For specific model values, see the [available models list](g://box-ai/supported-models)., defaults to None
        :type model: Optional[str], optional
        :param num_tokens_for_completion: The number of tokens for completion., defaults to None
        :type num_tokens_for_completion: Optional[int], optional
        """
        super().__init__(
            model=model,
            num_tokens_for_completion=num_tokens_for_completion,
            llm_endpoint_params=llm_endpoint_params,
            **kwargs
        )
