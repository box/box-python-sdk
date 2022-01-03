# coding: utf-8

import pytest

from mock import Mock
from boxsdk.config import API
from boxsdk.object.device_pinner import DevicePinner
from boxsdk.network.default_network import DefaultNetworkResponse


@pytest.fixture(scope='module')
def delete_device_pin_response():
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.ok = True
    return mock_network_response


def test_get(test_device_pin, mock_box_session):
    created_at = '2016-05-18T17:38:03-07:00'
    expected_url = f'{API.BASE_API_URL}/device_pinners/{test_device_pin.object_id}'
    mock_box_session.get.return_value.json.return_value = {
        'type': 'device_pinner',
        'id': test_device_pin.object_id,
        'created_at': created_at
    }
    device_pin = test_device_pin.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(device_pin, DevicePinner)
    assert device_pin.created_at == created_at


def test_delete_device_pin_return_the_correct_response(
        test_device_pin,
        mock_box_session,
        delete_device_pin_response,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.delete.return_value = delete_device_pin_response
    response = test_device_pin.delete()
    # pylint:disable=protected-access
    expected_url = test_device_pin.get_url()
    # pylint:enable = protected-access
    mock_box_session.delete.assert_called_once_with(expected_url, params={}, expect_json_response=False, headers=None)
    assert response is True
