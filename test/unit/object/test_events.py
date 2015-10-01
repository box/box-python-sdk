# coding: utf-8

from __future__ import unicode_literals
import json
from mock import Mock
import pytest
from requests.exceptions import Timeout
from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.object.events import Events
from boxsdk.session.box_session import BoxResponse


@pytest.fixture()
def test_events(mock_box_session):
    return Events(mock_box_session)


@pytest.fixture()
def final_stream_position():
    return 1348790499820


@pytest.fixture()
def initial_stream_position():
    return 1348790499819


@pytest.fixture()
def empty_events_response(final_stream_position):
    # pylint:disable=redefined-outer-name
    mock_box_response = Mock(BoxResponse)
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_box_response.network_response = mock_network_response
    mock_box_response.json.return_value = mock_json = {'next_stream_position': final_stream_position, 'entries': []}
    mock_box_response.content = json.dumps(mock_json).encode()
    mock_box_response.status_code = 200
    mock_box_response.ok = True
    return mock_box_response


@pytest.fixture()
def long_poll_url(test_url):
    return test_url


@pytest.fixture()
def retry_timeout():
    return 610


@pytest.fixture()
def options_response(long_poll_url, retry_timeout, make_mock_box_request):
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        response={'entries': [{'url': long_poll_url, 'retry_timeout': retry_timeout}]},
    )
    return mock_box_response


@pytest.fixture()
def new_change_long_poll_response(make_mock_box_request):
    mock_box_response, _ = make_mock_box_request(
        response={'message': 'new_change'},
    )
    return mock_box_response


@pytest.fixture()
def reconnect_long_poll_response(make_mock_box_request):
    mock_box_response, _ = make_mock_box_request(
        response={'message': 'reconnect'},
    )
    return mock_box_response


@pytest.fixture()
def max_retries_long_poll_response(make_mock_box_request):
    mock_box_response, _ = make_mock_box_request(
        response={'message': 'max_retries'},
    )
    return mock_box_response


@pytest.fixture()
def mock_event():
    return {
        "type": "event",
        "event_id": "f82c3ba03e41f7e8a7608363cc6c0390183c3f83",
        "source": {
            "type": "folder",
            "id": "11446498",
        }
    }


@pytest.fixture()
def events_response(initial_stream_position, mock_event, make_mock_box_request):
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        response={"next_stream_position": initial_stream_position, "entries": [mock_event]},
    )
    return mock_box_response


def test_get_events(test_events, mock_box_session, events_response):
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value = events_response
    events = test_events.get_events()
    assert 'next_stream_position' in events


def test_generate_events_with_long_polling(
        test_events,
        mock_box_session,
        events_response,
        empty_events_response,
        initial_stream_position,
        long_poll_url,
        retry_timeout,
        options_response,
        new_change_long_poll_response,
        reconnect_long_poll_response,
        max_retries_long_poll_response,
        mock_event,
):
    # pylint:disable=redefined-outer-name
    expected_url = test_events.get_url()
    mock_box_session.options.return_value = options_response
    mock_box_session.get.side_effect = [
        events_response,  # initial call to get now stream position
        Timeout,
        reconnect_long_poll_response,
        max_retries_long_poll_response,
        new_change_long_poll_response,
        events_response,
        new_change_long_poll_response,
        empty_events_response,
    ]
    events = test_events.generate_events_with_long_polling()
    assert next(events) == mock_event
    with pytest.raises(StopIteration):
        next(events)
    events.close()
    mock_box_session.options.assert_called_with(expected_url)
    mock_box_session.get.assert_any_call(expected_url, params={'stream_position': 'now'})
    assert '/events' in expected_url
    mock_box_session.get.assert_any_call(
        expected_url,
        params={'limit': 100, 'stream_type': 'all', 'stream_position': initial_stream_position},
    )
    mock_box_session.get.assert_any_call(
        long_poll_url,
        timeout=retry_timeout,
        params={'stream_position': initial_stream_position},
    )
