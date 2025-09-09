from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.schemas.comment_full import CommentFull

from box_sdk_gen.box.errors import BoxSDKError


class CommentsOrderDirectionField(str, Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class CommentsOrderField(BaseObject):
    def __init__(
        self,
        *,
        by: Optional[str] = None,
        direction: Optional[CommentsOrderDirectionField] = None,
        **kwargs
    ):
        """
        :param by: The field to order by., defaults to None
        :type by: Optional[str], optional
        :param direction: The direction to order by, either ascending or descending., defaults to None
        :type direction: Optional[CommentsOrderDirectionField], optional
        """
        super().__init__(**kwargs)
        self.by = by
        self.direction = direction


class Comments(BaseObject):
    def __init__(
        self,
        *,
        total_count: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order: Optional[List[CommentsOrderField]] = None,
        entries: Optional[List[CommentFull]] = None,
        **kwargs
    ):
        """
                :param total_count: One greater than the offset of the last entry in the entire collection.
        The total number of entries in the collection may be less than
        `total_count`.

        This field is only returned for calls that use offset-based pagination.
        For marker-based paginated APIs, this field will be omitted., defaults to None
                :type total_count: Optional[int], optional
                :param limit: The limit that was used for these entries. This will be the same as the
        `limit` query parameter unless that value exceeded the maximum value
        allowed. The maximum value varies by API., defaults to None
                :type limit: Optional[int], optional
                :param offset: The 0-based offset of the first entry in this set. This will be the same
        as the `offset` query parameter.

        This field is only returned for calls that use offset-based pagination.
        For marker-based paginated APIs, this field will be omitted., defaults to None
                :type offset: Optional[int], optional
                :param order: The order by which items are returned.

        This field is only returned for calls that use offset-based pagination.
        For marker-based paginated APIs, this field will be omitted., defaults to None
                :type order: Optional[List[CommentsOrderField]], optional
                :param entries: A list of comments., defaults to None
                :type entries: Optional[List[CommentFull]], optional
        """
        super().__init__(**kwargs)
        self.total_count = total_count
        self.limit = limit
        self.offset = offset
        self.order = order
        self.entries = entries
