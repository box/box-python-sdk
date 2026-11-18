from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.user_base_v2026_r0 import UserBaseV2026R0

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class AiSessionV2026R0TypeField(str, Enum):
    AI_SESSION = 'ai_session'


class AiSessionV2026R0SourceField(str, Enum):
    API = 'api'


class AiSessionV2026R0(BaseObject):
    _discriminator = 'type', {'ai_session'}

    def __init__(
        self,
        id: str,
        created_by: UserBaseV2026R0,
        updated_by: UserBaseV2026R0,
        created_at: DateTime,
        updated_at: DateTime,
        *,
        type: AiSessionV2026R0TypeField = AiSessionV2026R0TypeField.AI_SESSION,
        name: Optional[str] = None,
        source: AiSessionV2026R0SourceField = AiSessionV2026R0SourceField.API,
        client_id: Optional[str] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for the AI session. This is also the A2A
        `contextId` for the conversation. Treat the value as opaque.
                :type id: str
                :param created_at: The date and time when the AI session was created.
                :type created_at: DateTime
                :param updated_at: The date and time when the AI session was last updated. It advances on
        each turn of session activity, so it also serves as the most recently
        used ordering.
                :type updated_at: DateTime
                :param type: The value is always `ai_session`., defaults to AiSessionV2026R0TypeField.AI_SESSION
                :type type: AiSessionV2026R0TypeField, optional
                :param name: The display name of the AI session. Sessions created through the A2A API
        are named automatically. The value is `null` only when no name was
        recorded., defaults to None
                :type name: Optional[str], optional
                :param source: The origin of the AI session. Currently always `api`. New values
        may be added, so clients must tolerate values they do not recognize., defaults to AiSessionV2026R0SourceField.API
                :type source: AiSessionV2026R0SourceField, optional
                :param client_id: The OAuth client ID of the application that created the AI session, as
        shown in the Developer Console. The value is `null` if the application is
        not known., defaults to None
                :type client_id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at
        self.type = type
        self.name = name
        self.source = source
        self.client_id = client_id
