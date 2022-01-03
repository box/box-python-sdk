# coding: utf-8

from collections import OrderedDict
from itertools import chain
import json
from typing import Optional, Union
from urllib.parse import urlunsplit, urlencode

from mock import Mock
import pytest
from requests.exceptions import Timeout

from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.object.events import Events, EventsStreamType, UserEventsStreamType
from boxsdk.object.event import Event
from boxsdk.object.folder import Folder
from boxsdk.session.box_response import BoxResponse


@pytest.fixture()
def test_events(mock_box_session):
    return Events(mock_box_session)


@pytest.fixture()
def final_stream_position():
    return 1348790499820


@pytest.fixture()
def initial_stream_position():
    return 1348790499819


# pylint:disable=no-member
# pylint isn't currently smart enough to recognize the class member that was
# added by the metaclass, when the metaclass was added by @add_metaclass() /
# with_metaclass().
STREAM_TYPES_AS_ENUM_INSTANCES = list(EventsStreamType.__members__.values())
# pylint:enable=no-member
STREAM_TYPES_AS_STRINGS = list(map(str, STREAM_TYPES_AS_ENUM_INSTANCES))


def test_events_stream_type_extended_enum_class_has_expected_members():
    assert len(STREAM_TYPES_AS_ENUM_INSTANCES) >= 4
    assert len(STREAM_TYPES_AS_STRINGS) >= 4
    assert 'all' in STREAM_TYPES_AS_STRINGS
    assert 'changes' in STREAM_TYPES_AS_STRINGS
    assert 'sync' in STREAM_TYPES_AS_STRINGS
    assert 'admin_logs' in STREAM_TYPES_AS_STRINGS


@pytest.fixture(
    scope='session',
    params=list(chain(
        [None],   # Default behavior of not passing any stream_type
        STREAM_TYPES_AS_ENUM_INSTANCES,   # Passing an enum instance
        STREAM_TYPES_AS_STRINGS,  # Passing an enum value

        # For forwards compatibility, make sure that it works to pass a string
        # value that is not a member of the enum.
        ['future_stream_type'],
    )),
)
def stream_type_param(request) -> Optional[Union[str, EventsStreamType]]:
    """The value to pass as an Event method's stream_type parameter.

    :return:
        The parameter value, or `None` if no value should be passed.
    """
    return request.param


@pytest.fixture()
def expected_stream_type(stream_type_param) -> str:
    """The stream type we expect to use.
    """
    if stream_type_param is None:
        return UserEventsStreamType.ALL
    return stream_type_param


@pytest.fixture()
def stream_type_kwargs(stream_type_param) -> dict:
    """The kwargs for stream_type to pass when invoking a method on `Events`.
    """
    if stream_type_param:
        return {'stream_type': stream_type_param}
    return {}


@pytest.fixture()
def expected_stream_type_params(expected_stream_type) -> OrderedDict:
    """The stream_type-related params that we expect to pass to request methods.
    """
    return OrderedDict(stream_type=expected_stream_type)


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
def long_poll_url(test_url, expected_stream_type_params):
    return urlunsplit(('', '', test_url, urlencode(expected_stream_type_params), ''))


@pytest.fixture()
def retry_timeout():
    return 610


@pytest.fixture()
def options_response_entry(long_poll_url, retry_timeout):
    return {'url': long_poll_url, 'retry_timeout': retry_timeout}


@pytest.fixture()
def options_response(options_response_entry, make_mock_box_request):
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        response={'entries': [options_response_entry]},
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
def mock_event_json():
    return {
        "type": "event",
        "event_id": "f82c3ba03e41f7e8a7608363cc6c0390183c3f83",
        "source": {
            "type": "folder",
            "id": "11446498",
        },
    }


@pytest.fixture()
def events_response(initial_stream_position, mock_event_json, make_mock_box_request):
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        response={"next_stream_position": initial_stream_position, "entries": [mock_event_json]},
    )
    return mock_box_response


def test_get_events(
        test_events,
        mock_box_session,
        events_response,
        stream_type_kwargs,
        expected_stream_type_params,
):
    # pylint:disable=redefined-outer-name
    expected_url = test_events.get_url()
    mock_box_session.get.return_value = events_response
    events = test_events.get_events(**stream_type_kwargs)
    assert 'next_stream_position' in events
    mock_box_session.get.assert_any_call(
        expected_url,
        params=dict(limit=100, stream_position=0, **expected_stream_type_params),
    )
    for event, json in zip(events['entries'], events_response.json.return_value['entries']):
        assert isinstance(event, Event)
        assert event.event_id == json['event_id']


@pytest.mark.parametrize("limit", [100, None])
def test_get_admin_events(
        test_events,
        mock_box_session,
        events_response,
        limit,
):
    # pylint:disable=redefined-outer-name
    expected_url = test_events.get_url()
    mock_box_session.get.return_value = events_response
    events = test_events.get_admin_events(
        limit=limit,
        stream_position=0,
        created_after='2019-07-01T22:02:24-07:00',
        created_before='2019-08-07T22:02:24-07:00',
        event_types=['ITEM_CREATE', "LOGIN"],
    )
    expected_params = dict(
        stream_position=0,
        created_after='2019-07-01T22:02:24-07:00',
        created_before='2019-08-07T22:02:24-07:00',
        event_type='ITEM_CREATE,LOGIN',
        stream_type='admin_logs',
    )
    if limit:
        expected_params = dict(
            stream_position=0,
            created_after='2019-07-01T22:02:24-07:00',
            created_before='2019-08-07T22:02:24-07:00',
            event_type='ITEM_CREATE,LOGIN',
            stream_type='admin_logs',
            limit=limit,
        )
    mock_box_session.get.assert_called_with(
        expected_url,
        params=expected_params
    )
    for event, json in zip(events['entries'], events_response.json.return_value['entries']):
        assert isinstance(event, Event)
        assert event.event_id == json['event_id']


@pytest.mark.parametrize("limit", [100, None])
def test_get_admin_events_streaming(
        test_events,
        mock_box_session,
        events_response,
        limit,
):
    # pylint:disable=redefined-outer-name
    expected_url = test_events.get_url()
    mock_box_session.get.return_value = events_response
    events = test_events.get_admin_events_streaming(
        limit=limit,
        stream_position=100,
        event_types=['ITEM_CREATE', "LOGIN"],
    )
    expected_params = dict(
        stream_type='admin_logs_streaming',
        stream_position=100,
        event_type='ITEM_CREATE,LOGIN',
    )
    if limit:
        expected_params = dict(
            stream_type='admin_logs_streaming',
            limit=limit,
            stream_position=100,
            event_type='ITEM_CREATE,LOGIN',
        )
    mock_box_session.get.assert_called_with(
        expected_url,
        params=expected_params
    )
    for event, json in zip(events['entries'], events_response.json.return_value['entries']):
        assert isinstance(event, Event)
        assert event.event_id == json['event_id']


def test_get_long_poll_options(
        mock_box_session,
        test_events,
        stream_type_kwargs,
        expected_stream_type_params,
        options_response,
        options_response_entry,
):
    expected_url = test_events.get_url()
    mock_box_session.options.return_value = options_response
    long_poll_options = test_events.get_long_poll_options(**stream_type_kwargs)
    mock_box_session.options.assert_called_with(expected_url, params=expected_stream_type_params)
    assert long_poll_options == options_response_entry


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
        mock_event_json,
        stream_type_kwargs,
        expected_stream_type,
        expected_stream_type_params,
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
        EscapeGenerator("A fake exception for the session to throw so that the generator won't block forever"),
    ]
    events = test_events.generate_events_with_long_polling(**stream_type_kwargs)

    event = next(events)
    assert isinstance(event, Event)
    assert event.event_id == mock_event_json['event_id']
    assert isinstance(event.source, Folder)
    assert event.source.id == mock_event_json['source']['id']
    with pytest.raises(EscapeGenerator):
        next(events)
    events.close()
    mock_box_session.options.assert_called_with(expected_url, params=expected_stream_type_params)
    mock_box_session.get.assert_any_call(expected_url, params={'stream_position': 'now', 'limit': 0, 'stream_type': expected_stream_type})
    assert '/events' in expected_url
    mock_box_session.get.assert_any_call(
        expected_url,
        params=dict(limit=100, stream_position=initial_stream_position, **expected_stream_type_params),
    )
    mock_box_session.get.assert_any_call(
        long_poll_url,
        timeout=retry_timeout,
        params={'stream_position': initial_stream_position},
    )


class EscapeGenerator(RuntimeError):
    pass
