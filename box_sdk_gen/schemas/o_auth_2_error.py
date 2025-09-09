from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class OAuth2Error(BaseObject):
    def __init__(
        self,
        *,
        error: Optional[str] = None,
        error_description: Optional[str] = None,
        **kwargs
    ):
        """
        :param error: The type of the error returned., defaults to None
        :type error: Optional[str], optional
        :param error_description: The type of the error returned., defaults to None
        :type error_description: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.error = error
        self.error_description = error_description
