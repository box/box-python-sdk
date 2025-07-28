from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ArchiveV2025R0TypeField(str, Enum):
    ARCHIVE = 'archive'


class ArchiveV2025R0(BaseObject):
    _discriminator = 'type', {'archive'}

    def __init__(
        self,
        id: str,
        name: str,
        size: int,
        *,
        type: ArchiveV2025R0TypeField = ArchiveV2025R0TypeField.ARCHIVE,
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
                :param type: The value will always be `archive`., defaults to ArchiveV2025R0TypeField.ARCHIVE
                :type type: ArchiveV2025R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.name = name
        self.size = size
        self.type = type
