from typing import Optional

from box_sdk_gen.schemas.ai_llm_endpoint_params_open_ai import AiLlmEndpointParamsOpenAi

from box_sdk_gen.schemas.ai_llm_endpoint_params_google import AiLlmEndpointParamsGoogle

from box_sdk_gen.schemas.ai_llm_endpoint_params_aws import AiLlmEndpointParamsAws

from box_sdk_gen.schemas.ai_llm_endpoint_params_ibm import AiLlmEndpointParamsIbm

from box_sdk_gen.schemas.ai_llm_endpoint_params import AiLlmEndpointParams

from box_sdk_gen.schemas.ai_agent_basic_text_tool_base import AiAgentBasicTextToolBase

from box_sdk_gen.box.errors import BoxSDKError


class AiAgentBasicTextTool(AiAgentBasicTextToolBase):
    def __init__(
        self,
        *,
        system_message: Optional[str] = None,
        prompt_template: Optional[str] = None,
        model: Optional[str] = None,
        num_tokens_for_completion: Optional[int] = None,
        llm_endpoint_params: Optional[AiLlmEndpointParams] = None,
        **kwargs
    ):
        """
                :param system_message: System messages try to help the LLM "understand" its role and what it is supposed to do., defaults to None
                :type system_message: Optional[str], optional
                :param prompt_template: The prompt template contains contextual information of the request and the user prompt.
        When passing `prompt_template` parameters, you **must include** inputs for `{user_question}` and `{content}`.
        `{current_date}` is optional, depending on the use., defaults to None
                :type prompt_template: Optional[str], optional
                :param model: The model used for the AI agent for basic text. For specific model values, see the [available models list](g://box-ai/supported-models)., defaults to None
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
        self.system_message = system_message
        self.prompt_template = prompt_template
