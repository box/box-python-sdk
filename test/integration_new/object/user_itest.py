import time

import pytest

from boxsdk import BoxAPIException


def test_upload_and_delete_avatar(user, image_path):
    try:
        avatar_urls = user.upload_avatar(image_path)
        assert 'large' in avatar_urls and 'preview' in avatar_urls and 'small' in avatar_urls

        for _ in range(3):
            try:
                avatar = user.get_avatar()
            except BoxAPIException:
                time.sleep(1)
                continue
            break
        else:
            raise Exception("Cannot get avatar")

        assert avatar
    finally:
        user.delete_avatar()

    with pytest.raises(BoxAPIException):
        user.get_avatar()
