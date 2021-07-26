# coding: utf-8
from __future__ import unicode_literals

import json
import pytest

from boxsdk.config import API
from boxsdk.object.collaboration_whitelist_entry import CollaborationWhitelistEntry
from boxsdk.object.collaboration_whitelist_exempt_target import CollaborationWhitelistExemptTarget


def test_get_entries(mock_box_session, test_collaboration_whitelist):
    expected_url = '{0}/collaboration_whitelist_entries'.format(API.BASE_API_URL)
    mock_entry = {
        'type': 'collaboration_whitelist_entry',
        'id': '12345',
        'domain': 'box.com',
        'direction': 'both'
    }
    mock_box_session.get.return_value.json.return_value = {
        'limit': 100,
        'entries': [mock_entry]
    }
    entries = test_collaboration_whitelist.get_entries()
    entry = entries.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={})
    assert isinstance(entry, CollaborationWhitelistEntry)
    assert entry.id == mock_entry['id']
    assert entry.direction == mock_entry['direction']
    assert entry.domain == mock_entry['domain']


def test_get_exemptions(mock_box_session, test_collaboration_whitelist):
    expected_url = '{0}/collaboration_whitelist_exempt_targets'.format(API.BASE_API_URL)
    mock_exemption = {
        'type': 'collaboration_whitelist_exempt_target',
        'id': '12345',
        'user': {
            'type': 'user',
            'id': '33333'
        }
    }
    mock_box_session.get.return_value.json.return_value = {
        'limit': 100,
        'entries': [mock_exemption]
    }
    exemptions = test_collaboration_whitelist.get_exemptions()
    exemption = exemptions.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={})
    assert isinstance(exemption, CollaborationWhitelistExemptTarget)
    assert exemption.id == mock_exemption['id']
    assert exemption.user['id'] == mock_exemption['user']['id']


@pytest.mark.parametrize(
    'direction',
    ['inbound', 'outbound', 'both']
)
def test_add_domain(mock_box_session, test_collaboration_whitelist, direction):
    expected_url = '{0}/collaboration_whitelist_entries'.format(API.BASE_API_URL)
    domain = 'example.com'
    mock_entry = {
        'type': 'collaboration_whitelist_entry',
        'id': '12345',
        'domain': domain,
        'direction': direction
    }
    expected_data = {
        'domain': domain,
        'direction': direction
    }
    mock_box_session.post.return_value.json.return_value = mock_entry
    entry = test_collaboration_whitelist.add_domain(domain, direction)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data))
    assert isinstance(entry, CollaborationWhitelistEntry)
    assert entry.id == mock_entry['id']
    assert entry.domain == domain
    assert entry.direction == direction


def test_add_exemption(mock_box_session, test_collaboration_whitelist, mock_user):
    expected_url = '{0}/collaboration_whitelist_exempt_targets'.format(API.BASE_API_URL)
    expected_data = {
        'user': {
            'id': mock_user.object_id
        }
    }
    mock_exemption = {
        'type': 'collaboration_whitelist_exempt_target',
        'id': '12345',
        'user': {
            'type': 'user',
            'id': mock_user.object_id
        }
    }
    mock_box_session.post.return_value.json.return_value = mock_exemption
    exemption = test_collaboration_whitelist.add_exemption(mock_user)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data))
    assert exemption.id == mock_exemption['id']
    assert exemption.user['id'] == mock_exemption['user']['id']