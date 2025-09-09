from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.schemas.device_pinner import DevicePinner

from box_sdk_gen.box.errors import BoxSDKError


class DevicePinnersOrderByField(str, Enum):
    ID = 'id'


class DevicePinnersOrderDirectionField(str, Enum):
    ASC = 'asc'
    DESC = 'desc'


class DevicePinnersOrderField(BaseObject):
    def __init__(
        self,
        *,
        by: Optional[DevicePinnersOrderByField] = None,
        direction: Optional[DevicePinnersOrderDirectionField] = None,
        **kwargs
    ):
        """
        :param by: The field that is ordered by., defaults to None
        :type by: Optional[DevicePinnersOrderByField], optional
        :param direction: The direction to order by, either ascending or descending., defaults to None
        :type direction: Optional[DevicePinnersOrderDirectionField], optional
        """
        super().__init__(**kwargs)
        self.by = by
        self.direction = direction


class DevicePinners(BaseObject):
    def __init__(
        self,
        *,
        entries: Optional[List[DevicePinner]] = None,
        limit: Optional[int] = None,
        next_marker: Optional[int] = None,
        order: Optional[List[DevicePinnersOrderField]] = None,
        **kwargs
    ):
        """
                :param entries: A list of device pins., defaults to None
                :type entries: Optional[List[DevicePinner]], optional
                :param limit: The limit that was used for these entries. This will be the same as the
        `limit` query parameter unless that value exceeded the maximum value
        allowed., defaults to None
                :type limit: Optional[int], optional
                :param next_marker: The marker for the start of the next page of results., defaults to None
                :type next_marker: Optional[int], optional
                :param order: The order by which items are returned., defaults to None
                :type order: Optional[List[DevicePinnersOrderField]], optional
        """
        super().__init__(**kwargs)
        self.entries = entries
        self.limit = limit
        self.next_marker = next_marker
        self.order = order
