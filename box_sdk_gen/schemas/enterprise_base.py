from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class EnterpriseBaseTypeField(str, Enum):
    ENTERPRISE = 'enterprise'


class EnterpriseBase(BaseObject):
    _discriminator = 'type', {'enterprise'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[EnterpriseBaseTypeField] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this enterprise., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `enterprise`., defaults to None
        :type type: Optional[EnterpriseBaseTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
