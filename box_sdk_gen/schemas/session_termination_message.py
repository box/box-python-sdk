from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SessionTerminationMessage(BaseObject):
    def __init__(self, *, message: Optional[str] = None, **kwargs):
        """
        :param message: The unique identifier for the termination job status., defaults to None
        :type message: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.message = message
