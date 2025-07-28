from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.terms_of_service_user_status import TermsOfServiceUserStatus

from box_sdk_gen.box.errors import BoxSDKError


class TermsOfServiceUserStatuses(BaseObject):
    def __init__(
        self,
        *,
        total_count: Optional[int] = None,
        entries: Optional[List[TermsOfServiceUserStatus]] = None,
        **kwargs
    ):
        """
        :param total_count: The total number of objects., defaults to None
        :type total_count: Optional[int], optional
        :param entries: A list of terms of service user statuses., defaults to None
        :type entries: Optional[List[TermsOfServiceUserStatus]], optional
        """
        super().__init__(**kwargs)
        self.total_count = total_count
        self.entries = entries
