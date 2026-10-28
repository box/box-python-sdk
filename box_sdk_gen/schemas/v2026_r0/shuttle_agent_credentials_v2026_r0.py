from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class ShuttleAgentCredentialsV2026R0(BaseObject):
    def __init__(self, registration_token: str, expires_at: DateTime, **kwargs):
        """
                :param registration_token: The installation token to paste into the Windows agent installer to
        register the agent.
                :type registration_token: str
                :param expires_at: When the registration token expires and can no longer be used.
                :type expires_at: DateTime
        """
        super().__init__(**kwargs)
        self.registration_token = registration_token
        self.expires_at = expires_at
