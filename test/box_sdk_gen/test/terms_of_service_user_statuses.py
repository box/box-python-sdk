from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.terms_of_service import TermsOfService

from box_sdk_gen.schemas.user_full import UserFull

from box_sdk_gen.schemas.terms_of_service_user_status import TermsOfServiceUserStatus

from box_sdk_gen.managers.terms_of_service_user_statuses import (
    CreateTermsOfServiceStatusForUserTos,
)

from box_sdk_gen.managers.terms_of_service_user_statuses import (
    CreateTermsOfServiceStatusForUserUser,
)

from box_sdk_gen.schemas.terms_of_service_user_statuses import (
    TermsOfServiceUserStatuses,
)

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject

from test.box_sdk_gen.test.commons import get_or_create_terms_of_services

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import get_env_var


def testGetTermsOfServiceUserStatuses():
    admin_user_id: str = get_env_var('USER_ID')
    client: BoxClient = get_default_client_with_user_subject(admin_user_id)
    tos: TermsOfService = get_or_create_terms_of_services()
    user: UserFull = client.users.create_user(
        get_uuid(),
        login=''.join([get_uuid(), '@boxdemo.com']),
        is_platform_access_only=True,
    )
    created_tos_user_status: TermsOfServiceUserStatus = (
        client.terms_of_service_user_statuses.create_terms_of_service_status_for_user(
            CreateTermsOfServiceStatusForUserTos(id=tos.id),
            CreateTermsOfServiceStatusForUserUser(id=user.id),
            False,
        )
    )
    assert created_tos_user_status.is_accepted == False
    assert to_string(created_tos_user_status.type) == 'terms_of_service_user_status'
    assert to_string(created_tos_user_status.tos.type) == 'terms_of_service'
    assert to_string(created_tos_user_status.user.type) == 'user'
    assert created_tos_user_status.tos.id == tos.id
    assert created_tos_user_status.user.id == user.id
    updated_tos_user_status: TermsOfServiceUserStatus = (
        client.terms_of_service_user_statuses.update_terms_of_service_status_for_user_by_id(
            created_tos_user_status.id, True
        )
    )
    assert updated_tos_user_status.is_accepted == True
    list_tos_user_statuses: TermsOfServiceUserStatuses = (
        client.terms_of_service_user_statuses.get_terms_of_service_user_statuses(
            tos.id, user_id=user.id
        )
    )
    assert list_tos_user_statuses.total_count > 0
    client.users.delete_user_by_id(user.id)
