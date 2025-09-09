from typing import Optional

from typing import List

from box_sdk_gen.schemas.ai_llm_endpoint_params_open_ai import AiLlmEndpointParamsOpenAi

from box_sdk_gen.schemas.ai_llm_endpoint_params_google import AiLlmEndpointParamsGoogle

from box_sdk_gen.schemas.ai_llm_endpoint_params_aws import AiLlmEndpointParamsAws

from box_sdk_gen.schemas.ai_llm_endpoint_params_ibm import AiLlmEndpointParamsIbm

from box_sdk_gen.schemas.ai_llm_endpoint_params import AiLlmEndpointParams

from box_sdk_gen.schemas.ai_agent_basic_text_tool_base import AiAgentBasicTextToolBase

from box_sdk_gen.schemas.ai_agent_basic_text_tool import AiAgentBasicTextTool

from box_sdk_gen.schemas.ai_agent_long_text_tool import (
    AiAgentLongTextToolEmbeddingsField,
)

from box_sdk_gen.schemas.ai_agent_long_text_tool import AiAgentLongTextTool

from box_sdk_gen.schemas.ai_studio_agent_long_text_tool import AiStudioAgentLongTextTool

from box_sdk_gen.box.errors import BoxSDKError


class AiStudioAgentLongTextToolResponse(AiStudioAgentLongTextTool):
    def __init__(
        self,
        *,
        warnings: Optional[List[str]] = None,
        is_custom_instructions_included: Optional[bool] = None,
        embeddings: Optional[AiAgentLongTextToolEmbeddingsField] = None,
        system_message: Optional[str] = None,
        prompt_template: Optional[str] = None,
        model: Optional[str] = None,
        num_tokens_for_completion: Optional[int] = None,
        llm_endpoint_params: Optional[AiLlmEndpointParams] = None,
        **kwargs
    ):
        """
                :param warnings: Warnings concerning tool., defaults to None
                :type warnings: Optional[List[str]], optional
                :param is_custom_instructions_included: True if system message contains custom instructions placeholder, false otherwise., defaults to None
                :type is_custom_instructions_included: Optional[bool], optional
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
            is_custom_instructions_included=is_custom_instructions_included,
            embeddings=embeddings,
            system_message=system_message,
            prompt_template=prompt_template,
            model=model,
            num_tokens_for_completion=num_tokens_for_completion,
            llm_endpoint_params=llm_endpoint_params,
            **kwargs
        )
        self.warnings = warnings
