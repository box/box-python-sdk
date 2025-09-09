from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.schemas.user_full import UserFull

from box_sdk_gen.box.errors import BoxSDKError


class UsersOrderDirectionField(str, Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class UsersOrderField(BaseObject):
    def __init__(
        self,
        *,
        by: Optional[str] = None,
        direction: Optional[UsersOrderDirectionField] = None,
        **kwargs
    ):
        """
        :param by: The field to order by., defaults to None
        :type by: Optional[str], optional
        :param direction: The direction to order by, either ascending or descending., defaults to None
        :type direction: Optional[UsersOrderDirectionField], optional
        """
        super().__init__(**kwargs)
        self.by = by
        self.direction = direction


class Users(BaseObject):
    def __init__(
        self,
        *,
        limit: Optional[int] = None,
        next_marker: Optional[str] = None,
        prev_marker: Optional[str] = None,
        total_count: Optional[int] = None,
        offset: Optional[int] = None,
        order: Optional[List[UsersOrderField]] = None,
        entries: Optional[List[UserFull]] = None,
        **kwargs
    ):
        """
                :param limit: The limit that was used for these entries. This will be the same as the
        `limit` query parameter unless that value exceeded the maximum value
        allowed. The maximum value varies by API., defaults to None
                :type limit: Optional[int], optional
                :param next_marker: The marker for the start of the next page of results., defaults to None
                :type next_marker: Optional[str], optional
                :param prev_marker: The marker for the start of the previous page of results., defaults to None
                :type prev_marker: Optional[str], optional
                :param total_count: One greater than the offset of the last entry in the entire collection.
        The total number of entries in the collection may be less than
        `total_count`.

        This field is only returned for calls that use offset-based pagination.
        For marker-based paginated APIs, this field will be omitted., defaults to None
                :type total_count: Optional[int], optional
                :param offset: The 0-based offset of the first entry in this set. This will be the same
        as the `offset` query parameter.

        This field is only returned for calls that use offset-based pagination.
        For marker-based paginated APIs, this field will be omitted., defaults to None
                :type offset: Optional[int], optional
                :param order: The order by which items are returned.

        This field is only returned for calls that use offset-based pagination.
        For marker-based paginated APIs, this field will be omitted., defaults to None
                :type order: Optional[List[UsersOrderField]], optional
                :param entries: A list of users., defaults to None
                :type entries: Optional[List[UserFull]], optional
        """
        super().__init__(**kwargs)
        self.limit = limit
        self.next_marker = next_marker
        self.prev_marker = prev_marker
        self.total_count = total_count
        self.offset = offset
        self.order = order
        self.entries = entries
