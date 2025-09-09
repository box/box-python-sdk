from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class AiLlmEndpointParamsAwsTypeField(str, Enum):
    AWS_PARAMS = 'aws_params'


class AiLlmEndpointParamsAws(BaseObject):
    _discriminator = 'type', {'aws_params'}

    def __init__(
        self,
        *,
        type: AiLlmEndpointParamsAwsTypeField = AiLlmEndpointParamsAwsTypeField.AWS_PARAMS,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        **kwargs
    ):
        """
                :param type: The type of the AI LLM endpoint params object for AWS.
        This parameter is **required**., defaults to AiLlmEndpointParamsAwsTypeField.AWS_PARAMS
                :type type: AiLlmEndpointParamsAwsTypeField, optional
                :param temperature: What sampling temperature to use, between 0 and 1. Higher values like 0.8 will make the output more random,
        while lower values like 0.2 will make it more focused and deterministic.
        We generally recommend altering this or `top_p` but not both., defaults to None
                :type temperature: Optional[float], optional
                :param top_p: An alternative to sampling with temperature, called nucleus sampling, where the model considers the results
        of the tokens with `top_p` probability mass. So 0.1 means only the tokens comprising the top 10% probability
        mass are considered. We generally recommend altering this or temperature but not both., defaults to None
                :type top_p: Optional[float], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.temperature = temperature
        self.top_p = top_p
