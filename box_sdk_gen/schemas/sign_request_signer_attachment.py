from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestSignerAttachment(BaseObject):
    def __init__(
        self, *, id: Optional[str] = None, name: Optional[str] = None, **kwargs
    ):
        """
        :param id: Identifier of the attachment file., defaults to None
        :type id: Optional[str], optional
        :param name: Display name of the attachment file., defaults to None
        :type name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.name = name
