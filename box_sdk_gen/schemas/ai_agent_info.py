from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.box.errors import BoxSDKError


class AiAgentInfoModelsField(BaseObject):
    def __init__(
        self,
        *,
        name: Optional[str] = None,
        provider: Optional[str] = None,
        supported_purpose: Optional[str] = None,
        **kwargs
    ):
        """
        :param name: The name of the model used for the request., defaults to None
        :type name: Optional[str], optional
        :param provider: The provider that owns the model used for the request., defaults to None
        :type provider: Optional[str], optional
        :param supported_purpose: The supported purpose utilized by the model used for the request., defaults to None
        :type supported_purpose: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.name = name
        self.provider = provider
        self.supported_purpose = supported_purpose


class AiAgentInfo(BaseObject):
    def __init__(
        self,
        *,
        models: Optional[List[AiAgentInfoModelsField]] = None,
        processor: Optional[str] = None,
        **kwargs
    ):
        """
        :param models: The models used for the request., defaults to None
        :type models: Optional[List[AiAgentInfoModelsField]], optional
        :param processor: The processor used for the request., defaults to None
        :type processor: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.models = models
        self.processor = processor
