from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class ShieldRuleItemV2025R0TypeField(str, Enum):
    SHIELD_RULE = 'shield_rule'


class ShieldRuleItemV2025R0PriorityField(str, Enum):
    INFORMATIONAL = 'informational'
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'


class ShieldRuleItemV2025R0(BaseObject):
    _discriminator = 'type', {'shield_rule'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[ShieldRuleItemV2025R0TypeField] = None,
        rule_category: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[ShieldRuleItemV2025R0PriorityField] = None,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        **kwargs
    ):
        """
        :param id: The identifier of the shield rule., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `shield_rule`., defaults to None
        :type type: Optional[ShieldRuleItemV2025R0TypeField], optional
        :param rule_category: The category of the shield rule., defaults to None
        :type rule_category: Optional[str], optional
        :param name: The name of the shield rule., defaults to None
        :type name: Optional[str], optional
        :param description: The description of the shield rule., defaults to None
        :type description: Optional[str], optional
        :param priority: The priority level of the shield rule., defaults to None
        :type priority: Optional[ShieldRuleItemV2025R0PriorityField], optional
        :param created_at: The date and time when the shield rule was created., defaults to None
        :type created_at: Optional[DateTime], optional
        :param modified_at: The date and time when the shield rule was last modified., defaults to None
        :type modified_at: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.rule_category = rule_category
        self.name = name
        self.description = description
        self.priority = priority
        self.created_at = created_at
        self.modified_at = modified_at
