# coding: utf-8

from __future__ import unicode_literals
from mock import call, patch
import pytest
from boxsdk.config import API, Client
from boxsdk.object.group_membership import GroupMembership
from boxsdk.object.user import User


@pytest.fixture
def as_user_headers(mock_user_id, access_token):
    return {
        'Authorization': 'Bearer {0}'.format(access_token),
        'As-User': mock_user_id,
        'User-Agent': Client.USER_AGENT_STRING,
    }


def test_client_as_user_causes_as_user_header_to_be_added(
        box_client,
        mock_box_network,
        generic_successful_response,
        mock_user_id,
        as_user_headers,
):
    # pylint:disable=redefined-outer-name
    mock_box_network.session.request.side_effect = [generic_successful_response]
    box_client.as_user(User(None, mock_user_id)).folder('0').get()
    assert mock_box_network.session.request.mock_calls == [
        call(
            'GET',
            '{0}/folders/0'.format(API.BASE_API_URL),
            headers=as_user_headers,
            params=None,
        ),
    ]


def test_folder_object_as_user_causes_as_user_header_to_be_added(
        box_client,
        mock_box_network,
        generic_successful_response,
        mock_user_id,
        as_user_headers,
):
    # pylint:disable=redefined-outer-name
    mock_box_network.session.request.side_effect = [
        generic_successful_response,
    ]
    box_client.folder('0').as_user(User(None, mock_user_id)).get()
    assert mock_box_network.session.request.mock_calls == [
        call(
            'GET',
            '{0}/folders/0'.format(API.BASE_API_URL),
            headers=as_user_headers,
            params=None,
        ),
    ]


def test_group_membership_object_as_user_causes_as_user_header_to_be_added(
        box_client,
        mock_box_network,
        generic_successful_response,
        mock_user_id,
        as_user_headers,
):
    # pylint:disable=redefined-outer-name
    mock_box_network.session.request.side_effect = [
        generic_successful_response,
    ]
    with patch.object(GroupMembership, '_init_user_and_group_instances') as init:
        init.return_value = None, None
        box_client.group_membership('0').as_user(User(None, mock_user_id)).get()
    assert mock_box_network.session.request.mock_calls == [
        call(
            'GET',
            '{0}/group_memberships/0'.format(API.BASE_API_URL),
            headers=as_user_headers,
            params=None,
        ),
    ]


def test_events_endpoint_as_user_causes_as_user_header_to_be_added(
        box_client,
        mock_box_network,
        generic_successful_response,
        mock_user_id,
        as_user_headers,
):
    # pylint:disable=redefined-outer-name
    mock_box_network.session.request.side_effect = [
        generic_successful_response,
    ]
    stream_position = 1348790499819
    options = {'url': '{0}/events'.format(API.BASE_API_URL), 'retry_timeout': 60}
    box_client.events().as_user(User(None, mock_user_id)).long_poll(options, stream_position)
    assert mock_box_network.session.request.mock_calls == [
        call(
            'GET',
            options['url'],
            headers=as_user_headers,
            timeout=options['retry_timeout'],
            params={'stream_position': stream_position},
        ),
    ]


def test_metadata_endpoint_as_user_causes_as_user_header_to_be_added(
        box_client,
        mock_box_network,
        generic_successful_response,
        mock_user_id,
        as_user_headers,
):
    # pylint:disable=redefined-outer-name
    mock_box_network.session.request.side_effect = [
        generic_successful_response,
    ]
    box_client.file('0').metadata().as_user(User(None, mock_user_id)).get()
    assert mock_box_network.session.request.mock_calls == [
        call(
            'GET',
            '{0}/files/0/metadata/global/properties'.format(API.BASE_API_URL),
            headers=as_user_headers,
        ),
    ]
