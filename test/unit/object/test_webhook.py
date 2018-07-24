# coding: utf-8

from __future__ import unicode_literals
import json
import pytest
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
    # pylint:disable=protected-access
    expected_url = test_webhook.get_url()
    # pylint:enable = protected-access
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
