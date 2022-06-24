import pytest

from boxsdk import BoxAPIException


def test_upload_and_delete_avatar(user, image_path):

    avatar_urls = user.upload_avatar(image_path)
    assert 'large' in avatar_urls and 'preview' in avatar_urls and 'small' in avatar_urls

    avatar = user.get_avatar()
    assert avatar

    user.delete_avatar()
    with pytest.raises(BoxAPIException):
        user.get_avatar()
