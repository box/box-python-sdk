from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShuttlePathEntryAccountScopeV2026R0TypeField(str, Enum):
    ACCOUNT = 'account'


class ShuttlePathEntryAccountScopeV2026R0(BaseObject):
    _discriminator = 'type', {'account'}

    def __init__(
        self,
        *,
        type: ShuttlePathEntryAccountScopeV2026R0TypeField = ShuttlePathEntryAccountScopeV2026R0TypeField.ACCOUNT,
        id: Optional[str] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
        **kwargs
    ):
        """
                :param type: The value will always be `account`., defaults to ShuttlePathEntryAccountScopeV2026R0TypeField.ACCOUNT
                :type type: ShuttlePathEntryAccountScopeV2026R0TypeField, optional
                :param id: The platform-native identifier of the account that owns this entry.
        `null` when the system does not provide one. This is not the path
        entry `id`. Maps to `account.id` on an account-scoped path mapping
        location., defaults to None
                :type id: Optional[str], optional
                :param email: The email of the account that owns this entry. This is a
        system-native identifier and is not always an RFC 5322 address.
        `null` when unknown. Maps to `account.email` on an account-scoped
        path mapping location., defaults to None
                :type email: Optional[str], optional
                :param name: The display name of the account that owns this entry. `null` when
        unknown. Maps to `account.name` on an account-scoped path mapping
        location., defaults to None
                :type name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id
        self.email = email
        self.name = name
