from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from typing import Optional

from box_sdk_gen.box.errors import BoxSDKError


class ArchiveV2025R0TypeField(str, Enum):
    ARCHIVE = 'archive'


class ArchiveV2025R0OwnedByField(BaseObject):
    def __init__(self, id: str, type: str, **kwargs):
        """
        :param id: The unique identifier that represents a user who owns the archive.
        :type id: str
        :param type: The value is always `user`.
        :type type: str
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class ArchiveV2025R0(BaseObject):
    _discriminator = 'type', {'archive'}

    def __init__(
        self,
        id: str,
        name: str,
        size: int,
        *,
        type: ArchiveV2025R0TypeField = ArchiveV2025R0TypeField.ARCHIVE,
        description: Optional[str] = None,
        owned_by: Optional[ArchiveV2025R0OwnedByField] = None,
        **kwargs
    ):
        r"""
                :param id: The unique identifier that represents an archive.
                :type id: str
                :param name: The name of the archive.

        The following restrictions to the archive name apply: names containing
        non-printable ASCII characters, forward and backward slashes
        (`/`, `\`), names with trailing spaces, and names `.` and `..` are
        not allowed.
                :type name: str
                :param size: The size of the archive in bytes.
                :type size: int
                :param type: The value is always `archive`., defaults to ArchiveV2025R0TypeField.ARCHIVE
                :type type: ArchiveV2025R0TypeField, optional
                :param description: The description of the archive., defaults to None
                :type description: Optional[str], optional
                :param owned_by: The part of an archive API response that describes the user who owns the archive., defaults to None
                :type owned_by: Optional[ArchiveV2025R0OwnedByField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.name = name
        self.size = size
        self.type = type
        self.description = description
        self.owned_by = owned_by
