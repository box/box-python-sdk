from typing import Optional

from box_sdk_gen.schemas.shield_information_barrier_segment_member_base import (
    ShieldInformationBarrierSegmentMemberBaseTypeField,
)

from box_sdk_gen.schemas.shield_information_barrier_segment_member_base import (
    ShieldInformationBarrierSegmentMemberBase,
)

from box_sdk_gen.schemas.user_base import UserBase

from box_sdk_gen.box.errors import BoxSDKError


class ShieldInformationBarrierSegmentMemberMini(
    ShieldInformationBarrierSegmentMemberBase
):
    def __init__(
        self,
        *,
        user: Optional[UserBase] = None,
        id: Optional[str] = None,
        type: Optional[ShieldInformationBarrierSegmentMemberBaseTypeField] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for the
        shield information barrier segment member., defaults to None
                :type id: Optional[str], optional
                :param type: The type of the shield information barrier segment member., defaults to None
                :type type: Optional[ShieldInformationBarrierSegmentMemberBaseTypeField], optional
        """
        super().__init__(id=id, type=type, **kwargs)
        self.user = user
