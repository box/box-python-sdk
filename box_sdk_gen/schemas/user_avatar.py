from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class UserAvatarPicUrlsField(BaseObject):
    def __init__(
        self,
        *,
        small: Optional[str] = None,
        large: Optional[str] = None,
        preview: Optional[str] = None,
        **kwargs
    ):
        """
        :param small: The location of a small-sized avatar., defaults to None
        :type small: Optional[str], optional
        :param large: The location of a large-sized avatar., defaults to None
        :type large: Optional[str], optional
        :param preview: The location of the avatar preview., defaults to None
        :type preview: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.small = small
        self.large = large
        self.preview = preview


class UserAvatar(BaseObject):
    def __init__(self, *, pic_urls: Optional[UserAvatarPicUrlsField] = None, **kwargs):
        """
        :param pic_urls: Represents an object with user avatar URLs., defaults to None
        :type pic_urls: Optional[UserAvatarPicUrlsField], optional
        """
        super().__init__(**kwargs)
        self.pic_urls = pic_urls
