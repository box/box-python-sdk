# coding: utf-8
from __future__ import unicode_literals
import json
import pytest
 # from dateutil.parser import parse
from mock import Mock
from boxsdk.config import API
from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.object.webhook import Webhook


@pytest.fixture(scope='module')
def delete_webhook_response():
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.ok = True
    return mock_network_response


def test_delete_webhook_return_the_correct_response(
        test_webhook,
        mock_box_session,
        delete_webhook_response,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.delete.return_value = delete_webhook_response
    response = test_webhook.delete()
    expected_url = test_webhook.get_url()
    mock_box_session.delete.assert_called_once_with(expected_url, params={}, expect_json_response=False, headers=None)
    assert response is True


def test_get(test_webhook, mock_box_session):
    expected_url = '{0}/webhooks/{1}'.format(API.BASE_API_URL, test_webhook.object_id)
    mock_box_session.get.return_value.json.return_value = {
        'type': 'webhook',
        'id': test_webhook.object_id,
    }
    webhook = test_webhook.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(webhook, Webhook)


def test_update(test_webhook, mock_box_session):
    expected_url = '{0}/webhooks/{1}'.format(API.BASE_API_URL, test_webhook.object_id)
    mock_box_session.put.return_value.json.return_value = {
        'type': 'webhook',
        'id': test_webhook.object_id,
    }
    data = {
        'address': 'https://testnotification.com'
    }
    webhook = test_webhook.update_info(data)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(data), headers=None, params=None)
    assert isinstance(webhook, Webhook)
@pytest.mark.parametrize(
    'signature_version,signature_algorithm,primary_key,secondary_key,expected_result',
    [
        ('1', 'HmacSHA256', 'SamplePrimaryKey', 'SampleSecondaryKey', True),
        ('1', 'HmacSHA256', 'SamplePrimaryKey', None, True),
        ('1', 'HmacSHA256', 'WrongPrimaryKey', 'SampleSecondaryKey', True),
        ('1', 'HmacSHA256', 'WrongPrimaryKey', 'WrongSecondaryKey', False),
        ('1', 'HmacSHA256', None, None, False),
        ('2', 'HmacSHA256', 'SamplePrimaryKey', 'SampleSecondaryKey', False),
        ('1', 'WrongAlgorithm', 'SamplePrimaryKey', 'SampleSecondaryKey', False),
    ]
)

def test_validate_message(signature_version, signature_algorithm, primary_key, secondary_key, expected_result):
    body = {
        'webhook': {
            'id': '1234567890',
        },
        'trigger': 'FILE.UPLOADED',
        'source': {
            'id': '1234567890',
            'type': 'file',
            'name': 'Test.txt',
        }
    }
    encoded_body = json.dumps(body, separators=(',', ':')).encode()
    headers = {
        'box-delivery-id': 'f96bb54b-ee16-4fc5-aa65-8c2d9e5b546f',
        'box-delivery-timestamp': '2020-01-01T00:00:00-07:00',
        'box-signature-algorithm': signature_algorithm,
        'box-signature-primary': '6TfeAW3A1PASkgboxxA5yqHNKOwFyMWuEXny/FPD5hI=',
        'box-signature-secondary': 'v+1CD1Jdo3muIcbpv5lxxgPglOqMfsNHPV899xWYydo=',
        'box-signature-version': signature_version,
    }
    is_validated = Webhook.validate_message(encoded_body, headers, primary_key, secondary_key)
    assert is_validated is expected_result
