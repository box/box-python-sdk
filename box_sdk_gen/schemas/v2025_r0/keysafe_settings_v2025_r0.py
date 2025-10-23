from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class KeysafeSettingsV2025R0(BaseObject):
    def __init__(
        self,
        *,
        keysafe_enabled: Optional[bool] = None,
        cloud_provider: Optional[str] = None,
        key_id: Optional[str] = None,
        account_id: Optional[str] = None,
        location_id: Optional[str] = None,
        project_id: Optional[str] = None,
        keyring_id: Optional[str] = None,
        **kwargs
    ):
        """
        :param keysafe_enabled: Whether KeySafe addon is enabled for the enterprise., defaults to None
        :type keysafe_enabled: Optional[bool], optional
        :param cloud_provider: The cloud provider., defaults to None
        :type cloud_provider: Optional[str], optional
        :param key_id: The key ID., defaults to None
        :type key_id: Optional[str], optional
        :param account_id: The account ID., defaults to None
        :type account_id: Optional[str], optional
        :param location_id: The location ID., defaults to None
        :type location_id: Optional[str], optional
        :param project_id: The project ID., defaults to None
        :type project_id: Optional[str], optional
        :param keyring_id: The key ring ID., defaults to None
        :type keyring_id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.keysafe_enabled = keysafe_enabled
        self.cloud_provider = cloud_provider
        self.key_id = key_id
        self.account_id = account_id
        self.location_id = location_id
        self.project_id = project_id
        self.keyring_id = keyring_id
