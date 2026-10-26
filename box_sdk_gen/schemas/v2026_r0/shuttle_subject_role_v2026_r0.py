from enum import Enum

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleSubjectRoleV2026R0(str, Enum):
    OWNER = 'owner'
    CREATOR = 'creator'
    UPDATER = 'updater'
    NAMESPACE_ACCOUNT = 'namespace_account'
    SHAREE = 'sharee'
    ACCOUNT_HOLDER = 'account_holder'
    UNKNOWN = 'unknown'
