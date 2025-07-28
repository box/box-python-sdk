from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.comment_base import CommentBaseTypeField

from box_sdk_gen.schemas.comment_base import CommentBase

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class CommentItemField(BaseObject):
    def __init__(
        self, *, id: Optional[str] = None, type: Optional[str] = None, **kwargs
    ):
        """
        :param id: The unique identifier for this object., defaults to None
        :type id: Optional[str], optional
        :param type: The type for this object., defaults to None
        :type type: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class Comment(CommentBase):
    def __init__(
        self,
        *,
        is_reply_comment: Optional[bool] = None,
        message: Optional[str] = None,
        created_by: Optional[UserMini] = None,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        item: Optional[CommentItemField] = None,
        id: Optional[str] = None,
        type: Optional[CommentBaseTypeField] = None,
        **kwargs
    ):
        """
                :param is_reply_comment: Whether or not this comment is a reply to another
        comment., defaults to None
                :type is_reply_comment: Optional[bool], optional
                :param message: The text of the comment, as provided by the user., defaults to None
                :type message: Optional[str], optional
                :param created_at: The time this comment was created., defaults to None
                :type created_at: Optional[DateTime], optional
                :param modified_at: The time this comment was last modified., defaults to None
                :type modified_at: Optional[DateTime], optional
                :param id: The unique identifier for this comment., defaults to None
                :type id: Optional[str], optional
                :param type: The value will always be `comment`., defaults to None
                :type type: Optional[CommentBaseTypeField], optional
        """
        super().__init__(id=id, type=type, **kwargs)
        self.is_reply_comment = is_reply_comment
        self.message = message
        self.created_by = created_by
        self.created_at = created_at
        self.modified_at = modified_at
        self.item = item
