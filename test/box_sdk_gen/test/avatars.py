import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.user_full import UserFull

from box_sdk_gen.schemas.user_avatar import UserAvatar

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.internal.utils import decode_base_64

from box_sdk_gen.internal.utils import get_env_var

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import buffer_equals

from box_sdk_gen.internal.utils import read_byte_stream

from box_sdk_gen.internal.utils import generate_byte_buffer

from box_sdk_gen.internal.utils import decode_base_64_byte_stream

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def testAvatars():
    user: UserFull = client.users.get_user_me()
    created_avatar: UserAvatar = client.avatars.create_user_avatar(
        user.id,
        decode_base_64_byte_stream(
            'iVBORw0KGgoAAAANSUhEUgAAAQAAAAEAAQMAAABmvDolAAAAA1BMVEW10NBjBBbqAAAAH0lEQVRoge3BAQ0AAADCoPdPbQ43oAAAAAAAAAAAvg0hAAABmmDh1QAAAABJRU5ErkJggg=='
        ),
        pic_file_name='avatar.png',
        pic_content_type='image/png',
    )
    assert not created_avatar.pic_urls.small == None
    assert not created_avatar.pic_urls.large == None
    assert not created_avatar.pic_urls.preview == None
    response: ByteStream = client.avatars.get_user_avatar(user.id)
    assert buffer_equals(read_byte_stream(response), generate_byte_buffer(0)) == False
    client.avatars.delete_user_avatar(user.id)
    with pytest.raises(Exception):
        client.avatars.get_user_avatar(user.id)
