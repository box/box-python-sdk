from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class WatermarkWatermarkField(BaseObject):
    def __init__(
        self,
        *,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        **kwargs
    ):
        """
        :param created_at: When this watermark was created., defaults to None
        :type created_at: Optional[DateTime], optional
        :param modified_at: When this task was modified., defaults to None
        :type modified_at: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.created_at = created_at
        self.modified_at = modified_at


class Watermark(BaseObject):
    def __init__(
        self, *, watermark: Optional[WatermarkWatermarkField] = None, **kwargs
    ):
        super().__init__(**kwargs)
        self.watermark = watermark
