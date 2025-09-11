from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class CommentBaseTypeField(str, Enum):
    COMMENT = 'comment'


class CommentBase(BaseObject):
    _discriminator = 'type', {'comment'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[CommentBaseTypeField] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this comment., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `comment`., defaults to None
        :type type: Optional[CommentBaseTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
