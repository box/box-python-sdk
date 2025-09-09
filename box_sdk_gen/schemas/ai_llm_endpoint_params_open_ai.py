from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class AiLlmEndpointParamsOpenAiTypeField(str, Enum):
    OPENAI_PARAMS = 'openai_params'


class AiLlmEndpointParamsOpenAi(BaseObject):
    _discriminator = 'type', {'openai_params'}

    def __init__(
        self,
        *,
        type: AiLlmEndpointParamsOpenAiTypeField = AiLlmEndpointParamsOpenAiTypeField.OPENAI_PARAMS,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        stop: Optional[str] = None,
        **kwargs
    ):
        """
                :param type: The type of the AI LLM endpoint params object for OpenAI.
        This parameter is **required**., defaults to AiLlmEndpointParamsOpenAiTypeField.OPENAI_PARAMS
                :type type: AiLlmEndpointParamsOpenAiTypeField, optional
                :param temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random,
        while lower values like 0.2 will make it more focused and deterministic.
        We generally recommend altering this or `top_p` but not both., defaults to None
                :type temperature: Optional[float], optional
                :param top_p: An alternative to sampling with temperature, called nucleus sampling, where the model considers the results
        of the tokens with `top_p` probability mass. So 0.1 means only the tokens comprising the top 10% probability
        mass are considered. We generally recommend altering this or temperature but not both., defaults to None
                :type top_p: Optional[float], optional
                :param frequency_penalty: A number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the
        text so far, decreasing the model's likelihood to repeat the same line verbatim., defaults to None
                :type frequency_penalty: Optional[float], optional
                :param presence_penalty: A number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics., defaults to None
                :type presence_penalty: Optional[float], optional
                :param stop: Up to 4 sequences where the API will stop generating further tokens., defaults to None
                :type stop: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.stop = stop
