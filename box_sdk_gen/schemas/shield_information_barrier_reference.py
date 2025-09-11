from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.shield_information_barrier_base import (
    ShieldInformationBarrierBase,
)

from box_sdk_gen.box.errors import BoxSDKError


class ShieldInformationBarrierReference(BaseObject):
    def __init__(
        self,
        *,
        shield_information_barrier: Optional[ShieldInformationBarrierBase] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.shield_information_barrier = shield_information_barrier
