from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class AiLlmEndpointParamsIbmTypeField(str, Enum):
    IBM_PARAMS = 'ibm_params'


class AiLlmEndpointParamsIbm(BaseObject):
    _discriminator = 'type', {'ibm_params'}

    def __init__(
        self,
        *,
        type: AiLlmEndpointParamsIbmTypeField = AiLlmEndpointParamsIbmTypeField.IBM_PARAMS,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[float] = None,
        **kwargs
    ):
        """
                :param type: The type of the AI LLM endpoint params object for IBM.
        This parameter is **required**., defaults to AiLlmEndpointParamsIbmTypeField.IBM_PARAMS
                :type type: AiLlmEndpointParamsIbmTypeField, optional
                :param temperature: What sampling temperature to use, between 0 and 1. Higher values like 0.8 will make the output more random,
        while lower values like 0.2 will make it more focused and deterministic.
        We generally recommend altering this or `top_p` but not both., defaults to None
                :type temperature: Optional[float], optional
                :param top_p: An alternative to sampling with temperature, called nucleus sampling, where the model considers the results
        of the tokens with `top_p` probability mass. So 0.1 means only the tokens comprising the top 10% probability
        mass are considered. We generally recommend altering this or temperature but not both., defaults to None
                :type top_p: Optional[float], optional
                :param top_k: `Top-K` changes how the model selects tokens for output. A low `top-K` means the next selected token is
        the most probable among all tokens in the model's vocabulary (also called greedy decoding),
        while a high `top-K` means that the next token is selected from among the three most probable tokens by using temperature., defaults to None
                :type top_k: Optional[float], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
