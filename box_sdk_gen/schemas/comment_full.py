from typing import Optional

from box_sdk_gen.schemas.comment_base import CommentBaseTypeField

from box_sdk_gen.schemas.comment_base import CommentBase

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.internal.utils import DateTime

from box_sdk_gen.schemas.comment import CommentItemField

from box_sdk_gen.schemas.comment import Comment

from box_sdk_gen.box.errors import BoxSDKError


class CommentFull(Comment):
    def __init__(
        self,
        *,
        tagged_message: Optional[str] = None,
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
                :param tagged_message: The string representing the comment text with
        @mentions included. @mention format is @[id:username]
        where `id` is user's Box ID and `username` is
        their display name., defaults to None
                :type tagged_message: Optional[str], optional
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
        super().__init__(
            is_reply_comment=is_reply_comment,
            message=message,
            created_by=created_by,
            created_at=created_at,
            modified_at=modified_at,
            item=item,
            id=id,
            type=type,
            **kwargs
        )
        self.tagged_message = tagged_message
