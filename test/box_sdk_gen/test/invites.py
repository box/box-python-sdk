from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.user_full import UserFull

from box_sdk_gen.schemas.invite import Invite

from box_sdk_gen.managers.invites import CreateInviteEnterprise

from box_sdk_gen.managers.invites import CreateInviteActionableBy

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import get_env_var

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject


def testInvites():
    user_id: str = get_env_var('USER_ID')
    client: BoxClient = get_default_client_with_user_subject(user_id)
    current_user: UserFull = client.users.get_user_me(fields=['enterprise'])
    email: str = get_env_var('BOX_EXTERNAL_USER_EMAIL')
    invitation: Invite = client.invites.create_invite(
        CreateInviteEnterprise(id=current_user.enterprise.id),
        CreateInviteActionableBy(login=email),
    )
    assert to_string(invitation.type) == 'invite'
    assert invitation.invited_to.id == current_user.enterprise.id
    assert invitation.actionable_by.login == email
    get_invitation: Invite = client.invites.get_invite_by_id(invitation.id)
    assert get_invitation.id == invitation.id
