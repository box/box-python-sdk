from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from typing import Optional

from box_sdk_gen.box.errors import BoxSDKError


class HubCollaborationCreateRequestV2025R0HubTypeField(str, Enum):
    HUBS = 'hubs'


class HubCollaborationCreateRequestV2025R0HubField(BaseObject):
    _discriminator = 'type', {'hubs'}

    def __init__(
        self,
        id: str,
        *,
        type: HubCollaborationCreateRequestV2025R0HubTypeField = HubCollaborationCreateRequestV2025R0HubTypeField.HUBS,
        **kwargs
    ):
        """
        :param id: ID of the object.
        :type id: str
        :param type: The value will always be `hubs`., defaults to HubCollaborationCreateRequestV2025R0HubTypeField.HUBS
        :type type: HubCollaborationCreateRequestV2025R0HubTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class HubCollaborationCreateRequestV2025R0AccessibleByField(BaseObject):
    def __init__(
        self,
        type: str,
        *,
        id: Optional[str] = None,
        login: Optional[str] = None,
        **kwargs
    ):
        """
                :param type: The type of collaborator to invite.
        Possible values are `user` or `group`.
                :type type: str
                :param id: The ID of the user or group.

        Alternatively, use `login` to specify a user by email
        address., defaults to None
                :type id: Optional[str], optional
                :param login: The email address of the user who gets access to the item.

        Alternatively, use `id` to specify a user by user ID., defaults to None
                :type login: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id
        self.login = login


class HubCollaborationCreateRequestV2025R0(BaseObject):
    def __init__(
        self,
        hub: HubCollaborationCreateRequestV2025R0HubField,
        accessible_by: HubCollaborationCreateRequestV2025R0AccessibleByField,
        role: str,
        **kwargs
    ):
        """
                :param hub: Box Hubs reference.
                :type hub: HubCollaborationCreateRequestV2025R0HubField
                :param accessible_by: The user or group who gets access to the item.
                :type accessible_by: HubCollaborationCreateRequestV2025R0AccessibleByField
                :param role: The level of access granted to a Box Hub.
        Possible values are `editor`, `viewer`, and `co-owner`.
                :type role: str
        """
        super().__init__(**kwargs)
        self.hub = hub
        self.accessible_by = accessible_by
        self.role = role
