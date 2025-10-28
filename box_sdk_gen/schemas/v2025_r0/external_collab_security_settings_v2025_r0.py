from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class ExternalCollabSecuritySettingsV2025R0(BaseObject):
    def __init__(
        self,
        *,
        denylist_domains: Optional[List[str]] = None,
        denylist_emails: Optional[List[str]] = None,
        allowlist_domains: Optional[List[str]] = None,
        allowlist_emails: Optional[List[str]] = None,
        state: Optional[str] = None,
        scheduled_status: Optional[str] = None,
        scheduled_at: Optional[DateTime] = None,
        factor_type_settings: Optional[str] = None,
        **kwargs
    ):
        """
        :param denylist_domains: List of domains that are not allowed for external collaboration. Applies if state is `denylist`., defaults to None
        :type denylist_domains: Optional[List[str]], optional
        :param denylist_emails: List of email addresses that are not allowed for external collaboration. Applies if state is `denylist`., defaults to None
        :type denylist_emails: Optional[List[str]], optional
        :param allowlist_domains: List of domains that are allowed for external collaboration. Applies if state is `allowlist`., defaults to None
        :type allowlist_domains: Optional[List[str]], optional
        :param allowlist_emails: List of email addresses that are allowed for external collaboration. Applies if state is `allowlist`., defaults to None
        :type allowlist_emails: Optional[List[str]], optional
        :param state: The state of the external collaboration security settings. Possible values include `enabled`, `disabled`, `allowlist`, and `denylist`., defaults to None
        :type state: Optional[str], optional
        :param scheduled_status: The status of the scheduling to apply external collaboration security settings. Possible values include `in_progress`, `scheduled`, `completed`, `failed`, and `scheduled_immediate`., defaults to None
        :type scheduled_status: Optional[str], optional
        :param scheduled_at: Scheduled at., defaults to None
        :type scheduled_at: Optional[DateTime], optional
        :param factor_type_settings: Factor type for the external collaborators authentication. Possible values include `totp`, `any`, or `unknown`., defaults to None
        :type factor_type_settings: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.denylist_domains = denylist_domains
        self.denylist_emails = denylist_emails
        self.allowlist_domains = allowlist_domains
        self.allowlist_emails = allowlist_emails
        self.state = state
        self.scheduled_status = scheduled_status
        self.scheduled_at = scheduled_at
        self.factor_type_settings = factor_type_settings
