from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class UploadUrl(BaseObject):
    def __init__(
        self,
        *,
        upload_url: Optional[str] = None,
        upload_token: Optional[str] = None,
        **kwargs
    ):
        """
                :param upload_url: A URL for an upload session that can be used to upload
        the file., defaults to None
                :type upload_url: Optional[str], optional
                :param upload_token: An optional access token to use to upload the file., defaults to None
                :type upload_token: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.upload_url = upload_url
        self.upload_token = upload_token
