from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.enterprise_base import EnterpriseBase

from box_sdk_gen.schemas.user_base import UserBase

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class ShieldInformationBarrierTypeField(str, Enum):
    SHIELD_INFORMATION_BARRIER = 'shield_information_barrier'


class ShieldInformationBarrierStatusField(str, Enum):
    DRAFT = 'draft'
    PENDING = 'pending'
    DISABLED = 'disabled'
    ENABLED = 'enabled'
    INVALID = 'invalid'


class ShieldInformationBarrier(BaseObject):
    _discriminator = 'type', {'shield_information_barrier'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[ShieldInformationBarrierTypeField] = None,
        enterprise: Optional[EnterpriseBase] = None,
        status: Optional[ShieldInformationBarrierStatusField] = None,
        created_at: Optional[DateTime] = None,
        created_by: Optional[UserBase] = None,
        updated_at: Optional[DateTime] = None,
        updated_by: Optional[UserBase] = None,
        enabled_at: Optional[DateTime] = None,
        enabled_by: Optional[UserBase] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for the shield information barrier., defaults to None
                :type id: Optional[str], optional
                :param type: The type of the shield information barrier., defaults to None
                :type type: Optional[ShieldInformationBarrierTypeField], optional
                :param enterprise: The `type` and `id` of enterprise this barrier is under., defaults to None
                :type enterprise: Optional[EnterpriseBase], optional
                :param status: Status of the shield information barrier., defaults to None
                :type status: Optional[ShieldInformationBarrierStatusField], optional
                :param created_at: ISO date time string when this
        shield information barrier object was created., defaults to None
                :type created_at: Optional[DateTime], optional
                :param created_by: The user who created this shield information barrier., defaults to None
                :type created_by: Optional[UserBase], optional
                :param updated_at: ISO date time string when this shield information barrier was updated., defaults to None
                :type updated_at: Optional[DateTime], optional
                :param updated_by: The user that updated this shield information barrier., defaults to None
                :type updated_by: Optional[UserBase], optional
                :param enabled_at: ISO date time string when this shield information barrier was enabled., defaults to None
                :type enabled_at: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.enterprise = enterprise
        self.status = status
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by
        self.enabled_at = enabled_at
        self.enabled_by = enabled_by
