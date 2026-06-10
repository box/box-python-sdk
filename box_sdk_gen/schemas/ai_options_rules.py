from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class AiOptionsRules(BaseObject):
    def __init__(
        self,
        *,
        multi_select: Optional[bool] = None,
        selectable_levels: Optional[List[int]] = None,
        **kwargs
    ):
        """
                :param multi_select: Indicates whether the field is a multi-select field.
        If true, the field can have multiple values., defaults to None
                :type multi_select: Optional[bool], optional
                :param selectable_levels: The selectable levels for the field.
        This is used to limit the levels of the taxonomy that can be selected., defaults to None
                :type selectable_levels: Optional[List[int]], optional
        """
        super().__init__(**kwargs)
        self.multi_select = multi_select
        self.selectable_levels = selectable_levels
