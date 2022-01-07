# coding: utf-8

from mock import call
import pytest
from boxsdk.config import API, Client
from boxsdk.util.shared_link import get_shared_link_header


@pytest.fixture
def shared_link():
    return 'https://app.box.com/s/q2i1024dvguiads6mzj2avsq9hmz43du'


@pytest.fixture(params=(None, 'shared_link_password'))
def shared_link_password(request):
    return request.param


@pytest.fixture
def box_api_headers(shared_link, shared_link_password, access_token):
    # pylint:disable=redefined-outer-name
    box_api_header = get_shared_link_header(shared_link, shared_link_password)['BoxApi']
    return {
        'Authorization': f'Bearer {access_token}',
        'BoxApi': box_api_header,
        'User-Agent': Client.USER_AGENT_STRING,
        'X-Box-UA': Client.BOX_UA_STRING,
    }


def test_client_with_shared_link_causes_box_api_header_to_be_added(
        box_client,
        mock_box_network,
        generic_successful_response,
        shared_link,
        shared_link_password,
        box_api_headers,
):
    # pylint:disable=redefined-outer-name
    mock_box_network.session.request.side_effect = [
        generic_successful_response,
    ]
    box_client.with_shared_link(shared_link, shared_link_password).folder('0').get()
    assert mock_box_network.session.request.mock_calls == [
        call(
            'GET',
            f'{API.BASE_API_URL}/folders/0',
            headers=box_api_headers,
            params=None,
        ),
    ]


def test_folder_object_with_shared_link_causes_box_api_header_to_be_added(
        box_client,
        mock_box_network,
        generic_successful_response,
        shared_link,
        shared_link_password,
        box_api_headers,
):
    # pylint:disable=redefined-outer-name
    mock_box_network.session.request.side_effect = [
        generic_successful_response,
    ]
    box_client.folder('0').with_shared_link(shared_link, shared_link_password).get()
    assert mock_box_network.session.request.mock_calls == [
        call(
            'GET',
            f'{API.BASE_API_URL}/folders/0',
            headers=box_api_headers,
            params=None,
        ),
    ]


def test_group_membership_object_with_shared_link_causes_box_api_header_to_be_added(
        box_client,
        mock_box_network,
        generic_successful_response,
        shared_link,
        shared_link_password,
        box_api_headers,
):
    # pylint:disable=redefined-outer-name
    mock_box_network.session.request.side_effect = [
        generic_successful_response,
    ]
    box_client.group_membership('0').with_shared_link(shared_link, shared_link_password).get()
    assert mock_box_network.session.request.mock_calls == [
        call(
            'GET',
            f'{API.BASE_API_URL}/group_memberships/0',
            headers=box_api_headers,
            params=None,
        ),
    ]


def test_events_endpoint_with_shared_link_causes_box_api_header_to_be_added(
        box_client,
        mock_box_network,
        generic_successful_response,
        shared_link,
        shared_link_password,
        box_api_headers,
):
    # pylint:disable=redefined-outer-name
    mock_box_network.session.request.side_effect = [
        generic_successful_response,
    ]
    stream_position = 1348790499819
    options = {'url': f'{API.BASE_API_URL}/events', 'retry_timeout': 60}
    box_client.events().with_shared_link(shared_link, shared_link_password).long_poll(options, stream_position)
    assert mock_box_network.session.request.mock_calls == [
        call(
            'GET',
            options['url'],
            headers=box_api_headers,
            timeout=options['retry_timeout'],
            params={'stream_position': stream_position},
        ),
    ]


def test_metadata_endpoint_with_shared_link_causes_box_api_header_to_be_added(
        box_client,
        mock_box_network,
        generic_successful_response,
        shared_link,
        shared_link_password,
        box_api_headers,
):
    # pylint:disable=redefined-outer-name
    mock_box_network.session.request.side_effect = [
        generic_successful_response,
    ]
    box_client.file('0').metadata().with_shared_link(shared_link, shared_link_password).get()
    assert mock_box_network.session.request.mock_calls == [
        call(
            'GET',
            f'{API.BASE_API_URL}/files/0/metadata/global/properties',
            headers=box_api_headers,
        ),
    ]
