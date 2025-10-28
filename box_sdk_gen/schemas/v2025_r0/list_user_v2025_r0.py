from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ListUserV2025R0(BaseObject):
    def __init__(
        self,
        *,
        id: Optional[int] = None,
        name: Optional[str] = None,
        email: Optional[str] = None,
        **kwargs
    ):
        """
        :param id: The ID of the user., defaults to None
        :type id: Optional[int], optional
        :param name: The name of the user., defaults to None
        :type name: Optional[str], optional
        :param email: The email of the user., defaults to None
        :type email: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.name = name
        self.email = email
