from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.users import Users

from box_sdk_gen.schemas.user_full import UserFull

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import create_null

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def test_get_users():
    users: Users = client.users.get_users()
    assert users.total_count >= 0


def test_get_user_me():
    current_user: UserFull = client.users.get_user_me()
    assert to_string(current_user.type) == 'user'


def test_create_update_get_delete_user():
    user_name: str = get_uuid()
    user_login: str = ''.join([get_uuid(), '@gmail.com'])
    user: UserFull = client.users.create_user(
        user_name, login=user_login, is_platform_access_only=True
    )
    assert user.name == user_name
    user_by_id: UserFull = client.users.get_user_by_id(user.id)
    assert user_by_id.id == user.id
    updated_user_name: str = get_uuid()
    updated_user: UserFull = client.users.update_user_by_id(
        user.id, name=updated_user_name
    )
    assert updated_user.name == updated_user_name
    client.users.delete_user_by_id(user.id)
