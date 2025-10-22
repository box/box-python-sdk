from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class EnterpriseConfigurationItemV2025R0(BaseObject):
    def __init__(self, *, is_used: Optional[bool] = None, **kwargs):
        """
        :param is_used: Indicates whether a configuration is used for a given enterprise., defaults to None
        :type is_used: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.is_used = is_used
