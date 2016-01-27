# coding: utf-8

from __future__ import unicode_literals

from itertools import chain
import json

from mock import Mock
import pytest
from requests.exceptions import Timeout
from six.moves import map   # pylint:disable=redefined-builtin
from six.moves.urllib.parse import urlencode, urlunsplit  # pylint:disable=import-error,no-name-in-module

from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.object.events import Events, EventsStreamType, UserEventsStreamType
from boxsdk.session.box_session import BoxResponse
from boxsdk.util.ordered_dict import OrderedDict


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
def stream_type_param(request):
    """The value to pass as an Event method's stream_type parameter.

    :return:
        The parameter value, or `None` if no value should be passed.
    :rtype:
        :enum:`EventsStreamType` or `unicode` or `None`
    """
    return request.param


@pytest.fixture()
def expected_stream_type(stream_type_param):
    """The stream type we expect to use.

    :rtype:
        `unicode`
    """
    if stream_type_param is None:
        return UserEventsStreamType.ALL
    return stream_type_param


@pytest.fixture()
def stream_type_kwargs(stream_type_param):
    """The kwargs for stream_type to pass when invoking a method on `Events`.

    :rtype:
        `dict`
    """
    if stream_type_param:
        return {'stream_type': stream_type_param}
    return {}


@pytest.fixture()
def expected_stream_type_params(expected_stream_type):
    """The stream_type-related params that we expect to pass to request methods.

    :rtype:
        :class:`OrderedDict`
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
        mock_event,
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
    ]
    events = test_events.generate_events_with_long_polling(**stream_type_kwargs)
    assert next(events) == mock_event
    with pytest.raises(StopIteration):
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
