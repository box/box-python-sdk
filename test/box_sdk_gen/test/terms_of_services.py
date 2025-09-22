from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.terms_of_service import TermsOfService

from box_sdk_gen.managers.terms_of_services import UpdateTermsOfServiceByIdStatus

from box_sdk_gen.schemas.terms_of_services import TermsOfServices

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import get_or_create_terms_of_services

client: BoxClient = get_default_client()


def testGetTermsOfServices():
    tos: TermsOfService = get_or_create_terms_of_services()
    updated_tos_1: TermsOfService = (
        client.terms_of_services.update_terms_of_service_by_id(
            tos.id, UpdateTermsOfServiceByIdStatus.DISABLED, 'TOS'
        )
    )
    assert to_string(updated_tos_1.status) == 'disabled'
    assert updated_tos_1.text == 'TOS'
    updated_tos_2: TermsOfService = (
        client.terms_of_services.update_terms_of_service_by_id(
            tos.id, UpdateTermsOfServiceByIdStatus.DISABLED, 'Updated TOS'
        )
    )
    assert to_string(updated_tos_2.status) == 'disabled'
    assert updated_tos_2.text == 'Updated TOS'
    list_tos: TermsOfServices = client.terms_of_services.get_terms_of_service()
    assert list_tos.total_count > 0
