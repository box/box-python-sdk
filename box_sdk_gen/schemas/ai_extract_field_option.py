from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class AiExtractFieldOption(BaseObject):
    def __init__(self, key: str, **kwargs):
        """
        :param key: A unique identifier for the option.
        :type key: str
        """
        super().__init__(**kwargs)
        self.key = key
