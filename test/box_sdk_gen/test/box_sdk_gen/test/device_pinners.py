import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.device_pinners import DevicePinners

from box_sdk_gen.managers.device_pinners import GetEnterpriseDevicePinnersDirection

from test.box_sdk_gen.test.commons import get_default_client

from box_sdk_gen.internal.utils import get_env_var

client: BoxClient = get_default_client()


def testDevicePinners():
    enterprise_id: str = get_env_var('ENTERPRISE_ID')
    device_pinners: DevicePinners = client.device_pinners.get_enterprise_device_pinners(
        enterprise_id
    )
    assert len(device_pinners.entries) >= 0
    device_pinners_in_desc_direction: DevicePinners = (
        client.device_pinners.get_enterprise_device_pinners(
            enterprise_id, direction=GetEnterpriseDevicePinnersDirection.DESC
        )
    )
    assert len(device_pinners_in_desc_direction.entries) >= 0
    device_pinner_id: str = '123456'
    with pytest.raises(Exception):
        client.device_pinners.get_device_pinner_by_id(device_pinner_id)
    with pytest.raises(Exception):
        client.device_pinners.delete_device_pinner_by_id(device_pinner_id)
