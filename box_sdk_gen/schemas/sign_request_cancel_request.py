from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestCancelRequest(BaseObject):
    def __init__(self, *, reason: Optional[str] = None, **kwargs):
        """
        :param reason: An optional reason for cancelling the sign request., defaults to None
        :type reason: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.reason = reason
