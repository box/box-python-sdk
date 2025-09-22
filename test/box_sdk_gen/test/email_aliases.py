from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.user_full import UserFull

from box_sdk_gen.schemas.email_aliases import EmailAliases

from box_sdk_gen.schemas.email_alias import EmailAlias

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def testEmailAliases():
    new_user_name: str = get_uuid()
    new_user_login: str = ''.join([get_uuid(), '@boxdemo.com'])
    new_user: UserFull = client.users.create_user(new_user_name, login=new_user_login)
    aliases: EmailAliases = client.email_aliases.get_user_email_aliases(new_user.id)
    assert aliases.total_count == 0
    new_alias_email: str = ''.join([new_user.id, '@boxdemo.com'])
    new_alias: EmailAlias = client.email_aliases.create_user_email_alias(
        new_user.id, new_alias_email
    )
    updated_aliases: EmailAliases = client.email_aliases.get_user_email_aliases(
        new_user.id
    )
    assert updated_aliases.total_count == 1
    assert updated_aliases.entries[0].email == new_alias_email
    client.email_aliases.delete_user_email_alias_by_id(new_user.id, new_alias.id)
    final_aliases: EmailAliases = client.email_aliases.get_user_email_aliases(
        new_user.id
    )
    assert final_aliases.total_count == 0
    client.users.delete_user_by_id(new_user.id)
