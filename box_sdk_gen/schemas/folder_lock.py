from box_sdk_gen.internal.base_object import BaseObject

from typing import Optional

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.schemas.user_base import UserBase

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class FolderLockLockedOperationsField(BaseObject):
    def __init__(self, move: bool, delete: bool, **kwargs):
        """
        :param move: Whether moving the folder is restricted.
        :type move: bool
        :param delete: Whether deleting the folder is restricted.
        :type delete: bool
        """
        super().__init__(**kwargs)
        self.move = move
        self.delete = delete


class FolderLock(BaseObject):
    def __init__(
        self,
        *,
        folder: Optional[FolderMini] = None,
        id: Optional[str] = None,
        type: Optional[str] = None,
        created_by: Optional[UserBase] = None,
        created_at: Optional[DateTime] = None,
        locked_operations: Optional[FolderLockLockedOperationsField] = None,
        lock_type: Optional[str] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for this folder lock., defaults to None
                :type id: Optional[str], optional
                :param type: The object type, always `folder_lock`., defaults to None
                :type type: Optional[str], optional
                :param created_at: When the folder lock object was created., defaults to None
                :type created_at: Optional[DateTime], optional
                :param locked_operations: The operations that have been locked. Currently the `move`
        and `delete` operations cannot be locked separately, and both need to be
        set to `true`., defaults to None
                :type locked_operations: Optional[FolderLockLockedOperationsField], optional
                :param lock_type: The lock type, always `freeze`., defaults to None
                :type lock_type: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.folder = folder
        self.id = id
        self.type = type
        self.created_by = created_by
        self.created_at = created_at
        self.locked_operations = locked_operations
        self.lock_type = lock_type
