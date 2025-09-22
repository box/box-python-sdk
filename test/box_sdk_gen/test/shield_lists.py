from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.v2025_r0.shield_list_v2025_r0 import ShieldListV2025R0

from box_sdk_gen.schemas.v2025_r0.shield_list_content_country_v2025_r0 import (
    ShieldListContentCountryV2025R0TypeField,
)

from box_sdk_gen.schemas.v2025_r0.shield_list_content_domain_v2025_r0 import (
    ShieldListContentDomainV2025R0TypeField,
)

from box_sdk_gen.schemas.v2025_r0.shield_list_content_email_v2025_r0 import (
    ShieldListContentEmailV2025R0TypeField,
)

from box_sdk_gen.schemas.v2025_r0.shield_list_content_ip_v2025_r0 import (
    ShieldListContentIpV2025R0TypeField,
)

from box_sdk_gen.schemas.v2025_r0.shield_lists_v2025_r0 import ShieldListsV2025R0

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import get_env_var

from test.box_sdk_gen.test.commons import upload_new_file

from test.box_sdk_gen.test.commons import create_new_folder

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject

from box_sdk_gen.schemas.v2025_r0.shield_list_content_country_v2025_r0 import (
    ShieldListContentCountryV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.shield_list_content_domain_v2025_r0 import (
    ShieldListContentDomainV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.shield_list_content_email_v2025_r0 import (
    ShieldListContentEmailV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.shield_list_content_ip_v2025_r0 import (
    ShieldListContentIpV2025R0,
)

user_id: str = get_env_var('USER_ID')

client: BoxClient = get_default_client_with_user_subject(user_id)


def testCreateGetUpdateDeleteShieldList():
    shield_list_country_name: str = ''.join([get_uuid(), 'shieldListCountry'])
    shield_list_country: ShieldListV2025R0 = (
        client.shield_lists.create_shield_list_v2025_r0(
            shield_list_country_name,
            ShieldListContentCountryV2025R0(
                type=ShieldListContentCountryV2025R0TypeField.COUNTRY,
                country_codes=['US', 'PL'],
            ),
            description='A list of things that are shielded',
        )
    )
    shield_list_content_domain_name: str = ''.join(
        [get_uuid(), 'shieldListContentDomain']
    )
    shield_list_content_domain: ShieldListV2025R0 = (
        client.shield_lists.create_shield_list_v2025_r0(
            shield_list_content_domain_name,
            ShieldListContentDomainV2025R0(
                type=ShieldListContentDomainV2025R0TypeField.DOMAIN,
                domains=['box.com', 'example.com'],
            ),
            description='A list of things that are shielded',
        )
    )
    shield_list_content_email_name: str = ''.join(
        [get_uuid(), 'shieldListContentEmail']
    )
    shield_list_content_email: ShieldListV2025R0 = (
        client.shield_lists.create_shield_list_v2025_r0(
            shield_list_content_email_name,
            ShieldListContentEmailV2025R0(
                type=ShieldListContentEmailV2025R0TypeField.EMAIL,
                email_addresses=['test@box.com', 'test@example.com'],
            ),
            description='A list of things that are shielded',
        )
    )
    shield_list_content_ip_name: str = ''.join([get_uuid(), 'shieldListContentIp'])
    shield_list_content_ip: ShieldListV2025R0 = (
        client.shield_lists.create_shield_list_v2025_r0(
            shield_list_content_ip_name,
            ShieldListContentIpV2025R0(
                type=ShieldListContentIpV2025R0TypeField.IP,
                ip_addresses=['127.0.0.1', '80.12.12.12/24'],
            ),
            description='A list of things that are shielded',
        )
    )
    shield_lists: ShieldListsV2025R0 = client.shield_lists.get_shield_lists_v2025_r0()
    assert len(shield_lists.entries) > 0
    get_shield_list_country: ShieldListV2025R0 = (
        client.shield_lists.get_shield_list_by_id_v2025_r0(shield_list_country.id)
    )
    assert get_shield_list_country.name == shield_list_country_name
    assert get_shield_list_country.description == 'A list of things that are shielded'
    client.shield_lists.update_shield_list_by_id_v2025_r0(
        shield_list_country.id,
        shield_list_country_name,
        ShieldListContentCountryV2025R0(
            type=ShieldListContentCountryV2025R0TypeField.COUNTRY, country_codes=['US']
        ),
        description='Updated description',
    )
    get_shield_list_country_updated: ShieldListV2025R0 = (
        client.shield_lists.get_shield_list_by_id_v2025_r0(shield_list_country.id)
    )
    assert get_shield_list_country_updated.description == 'Updated description'
    client.shield_lists.delete_shield_list_by_id_v2025_r0(shield_list_country.id)
    client.shield_lists.delete_shield_list_by_id_v2025_r0(shield_list_content_domain.id)
    client.shield_lists.delete_shield_list_by_id_v2025_r0(shield_list_content_email.id)
    client.shield_lists.delete_shield_list_by_id_v2025_r0(shield_list_content_ip.id)
