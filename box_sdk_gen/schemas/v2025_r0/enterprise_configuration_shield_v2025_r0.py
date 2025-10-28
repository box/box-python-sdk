from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2025_r0.shield_rule_item_v2025_r0 import ShieldRuleItemV2025R0

from box_sdk_gen.box.errors import BoxSDKError


class EnterpriseConfigurationShieldV2025R0(BaseObject):
    def __init__(
        self, *, shield_rules: Optional[List[ShieldRuleItemV2025R0]] = None, **kwargs
    ):
        """
        :param shield_rules: The shield rules configuration for the enterprise., defaults to None
        :type shield_rules: Optional[List[ShieldRuleItemV2025R0]], optional
        """
        super().__init__(**kwargs)
        self.shield_rules = shield_rules
