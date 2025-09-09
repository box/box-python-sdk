from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class DocGenTagsProcessingMessageV2025R0(BaseObject):
    def __init__(self, message: str, **kwargs):
        """
        :param message: A message informing the user that document tags are still being processed.
        :type message: str
        """
        super().__init__(**kwargs)
        self.message = message
