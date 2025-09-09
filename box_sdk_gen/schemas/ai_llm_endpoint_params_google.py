from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class AiLlmEndpointParamsGoogleTypeField(str, Enum):
    GOOGLE_PARAMS = 'google_params'


class AiLlmEndpointParamsGoogle(BaseObject):
    _discriminator = 'type', {'google_params'}

    def __init__(
        self,
        *,
        type: AiLlmEndpointParamsGoogleTypeField = AiLlmEndpointParamsGoogleTypeField.GOOGLE_PARAMS,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[float] = None,
        **kwargs
    ):
        """
                :param type: The type of the AI LLM endpoint params object for Google.
        This parameter is **required**., defaults to AiLlmEndpointParamsGoogleTypeField.GOOGLE_PARAMS
                :type type: AiLlmEndpointParamsGoogleTypeField, optional
                :param temperature: The temperature is used for sampling during response generation, which occurs when `top-P` and `top-K` are applied. Temperature controls the degree of randomness in the token selection., defaults to None
                :type temperature: Optional[float], optional
                :param top_p: `Top-P` changes how the model selects tokens for output. Tokens are selected from the most (see `top-K`) to least probable until the sum of their probabilities equals the `top-P` value., defaults to None
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
