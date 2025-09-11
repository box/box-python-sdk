from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.email_alias import EmailAlias

from box_sdk_gen.box.errors import BoxSDKError


class EmailAliases(BaseObject):
    def __init__(
        self,
        *,
        total_count: Optional[int] = None,
        entries: Optional[List[EmailAlias]] = None,
        **kwargs
    ):
        """
        :param total_count: The number of email aliases., defaults to None
        :type total_count: Optional[int], optional
        :param entries: A list of email aliases., defaults to None
        :type entries: Optional[List[EmailAlias]], optional
        """
        super().__init__(**kwargs)
        self.total_count = total_count
        self.entries = entries
