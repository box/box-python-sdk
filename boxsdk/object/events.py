from datetime import datetime
from typing import Any, Optional, Iterable, Generator, Union, TYPE_CHECKING

from requests.exceptions import Timeout

from .base_endpoint import BaseEndpoint
from ..util.api_call_decorator import api_call
from ..util.datetime_formatter import normalize_date_to_rfc3339_format
from ..util.enum import ExtendableEnumMeta
from ..util.lru_cache import LRUCache
from ..util.text_enum import TextEnum

if TYPE_CHECKING:
    from boxsdk.object.event import Event
    from boxsdk.session.box_response import BoxResponse


# pylint:disable=too-many-ancestors
class EventsStreamType(TextEnum, metaclass=ExtendableEnumMeta):
    """An enum of all possible values of the `stream_type` parameter for user events.

    The value of the `stream_type` parameter determines the type of events
    returned by the endpoint.

    <https://developer.box.com/en/guides/events/>
    """


class UserEventsStreamType(EventsStreamType):
    """An enum of all possible values of the `stream_type` parameter for user events.

    - ALL: Returns all user events.
    - CHANGES: Returns tree changes.
    - SYNC: Returns tree changes only for sync folders.

    <https://developer.box.com/en/guides/events/for-user/>
    """
    ALL = 'all'
    CHANGES = 'changes'
    SYNC = 'sync'


class EnterpriseEventsStreamType(EventsStreamType):
    """An enum of all possible values of the `stream_type` parameter for enterprise events.

    - ADMIN_LOGS: Retrieves up to a year's events for all users in the enterprise. High latency.
    - ADMIN_LOGS_STREAMING: Retrieves up to a two weeks's events for all users in the enterprise. Low latency.

    NOTE: Requires Admin: These stream types will only work with an auth token
    from an enterprise admin account.

    <https://developer.box.com/en/guides/events/for-enterprise/>
    """
    ADMIN_LOGS = 'admin_logs'
    ADMIN_LOGS_STREAMING = 'admin_logs_streaming'
# pylint:enable=too-many-ancestors


class Events(BaseEndpoint):
    """Box API endpoint for subscribing to changes in a Box account."""

    def get_url(self, *args: Any) -> str:
        """Base class override."""
        return super().get_url('events', *args)

    @api_call
    def get_events(
            self,
            limit: int = 100,
            stream_position: Union[str, int] = 0,
            stream_type: EventsStreamType = UserEventsStreamType.ALL
    ) -> dict:
        """
        Get Box events from a given stream position for a given stream type.

        :param limit:
            Maximum number of events to return.
        :param stream_position:
            The location in the stream from which to start getting events. 0 is the beginning of time. 'now' will
            return no events and just current stream position.
        :param stream_type:
            (optional) Which type of events to return.
            Defaults to `UserEventsStreamType.ALL`.
        :returns:
            Dictionary containing the next stream position along with a list of some number of events.
        """
        url = self.get_url()
        params = {
            'limit': limit,
            'stream_position': stream_position,
            'stream_type': stream_type,
        }
        box_response = self._session.get(url, params=params)
        response = box_response.json().copy()
        return self.translator.translate(self._session, response_object=response)

    @api_call
    def get_admin_events(
            self,
            limit: Optional[int] = None,
            stream_position: Union[str, int] = 0,
            created_after: Union[datetime, str] = None,
            created_before: Union[datetime, str] = None,
            event_types: Iterable[str] = None
    ) -> dict:
        """
        Get Box Admin events from a datetime, to a datetime, or between datetimes with a given event type for a enterprise
        stream type. Used for historical querying (up to one year). Works for Enterprise admin_logs type.

        :param limit:
            (optional) Maximum number of events to return. If None, default API value limit=100 will be used.
        :param stream_position:
            The location in the stream from which to start getting events. 0 is the beginning of time.
        :param created_after:
            (optional) Start date in datetime format to pull events from
        :param created_before:
            (optional) End date in datetime format to pull events to
        :param event_types:
            (optional) Which events to return (ie. LOGIN)
        :returns:
            Dictionary containing the next stream position along with a list of some number of events.
        """
        url = self.get_url()
        params = {
            'created_after': normalize_date_to_rfc3339_format(created_after),
            'created_before': normalize_date_to_rfc3339_format(created_before),
            'stream_type': 'admin_logs',
        }
        if limit is not None:
            params['limit'] = limit
        if event_types is not None:
            params['event_type'] = ','.join(event_types)
        if stream_position is not None:
            params['stream_position'] = stream_position
        box_response = self._session.get(url, params=params)
        response = box_response.json()
        return self.translator.translate(self._session, response_object=response)

    @api_call
    def get_admin_events_streaming(
            self,
            limit: Optional[int] = None,
            stream_position: Union[str, int] = 0,
            event_types: Iterable[str] = None
    ) -> dict:
        """
        Get Box Admin events with a given event type for a enterprise stream type. Used for live monitoring (up to two weeks).
        Works for Enterprise admin_logs_streaming type.

        :param limit:
            (optional) Maximum number of events to return.
        :param stream_position:
            The location in the stream from which to start getting events. 0 is the beginning of time. 'now' will
            return no events and just current stream position.
        :param event_types:
            (optional) Which events to return (ie. LOGIN)
        :returns:
            Dictionary containing the next stream position along with a list of some number of events.
        """
        url = self.get_url()
        params = {
            'stream_type': 'admin_logs_streaming',
        }
        if limit is not None:
            params['limit'] = limit
        if stream_position is not None:
            params['stream_position'] = stream_position
        if event_types is not None:
            params['event_type'] = ','.join(event_types)
        box_response = self._session.get(url, params=params)
        response = box_response.json()
        return self.translator.translate(self._session, response_object=response)

    @api_call
    def get_latest_stream_position(self, stream_type: UserEventsStreamType = UserEventsStreamType.ALL) -> int:
        """
        Get the latest stream position. The return value can be used with :meth:`get_events` or
        :meth:`generate_events_with_long_polling`.

        :param stream_type:
            (optional) Which events stream to query.

            NOTE: Currently, the Box API requires this to be one of the user
            events stream types. The request will fail if an enterprise events
            stream type is passed.
        :returns:
            The latest stream position.
        """
        return self.get_events(limit=0, stream_position='now', stream_type=stream_type)['next_stream_position']

    def _get_all_events_since(
            self,
            stream_position: Union[str, int],
            stream_type: EventsStreamType = UserEventsStreamType.ALL
    ) -> Generator[tuple, None, None]:
        """
        :param stream_position:
            The location in the stream from which to start getting events. 0 is the beginning of time. 'now' will
            return no events and just current stream position.
        :param stream_type:
            (optional) Which type of events to return.
        """
        next_stream_position = stream_position
        while True:
            events = self.get_events(stream_position=next_stream_position, limit=100, stream_type=stream_type)
            next_stream_position = events['next_stream_position']
            events = events['entries']
            if not events:
                return
            for event in events:
                yield event, next_stream_position
            if len(events) < 100:
                return

    @api_call
    def long_poll(self, options: dict, stream_position: Union[str, int]) -> 'BoxResponse':
        """
        Set up a long poll connection at the specified url.

        :param options:
            The long poll options which include a long pull url, retry timeout, etc.
        :param stream_position:
            The location in the stream from which to start getting events. 0 is the beginning of time.
            'now' will return no events and just current stream position.
        :returns:
            {"message": "new_change"}, which means there're new changes on Box or {"version": 1, "message": "reconnect"}
            if nothing happens on Box during the long poll.
        """
        url = options['url']
        long_poll_response = self._session.get(
            url,
            timeout=options['retry_timeout'],
            params={'stream_position': stream_position}
        )
        return long_poll_response

    @api_call
    def generate_events_with_long_polling(
            self,
            stream_position: Union[str, int] = None,
            stream_type: UserEventsStreamType = UserEventsStreamType.ALL
    ) -> Generator['Event', None, None]:
        """
        Subscribe to events from the given stream position.

        :param stream_position:
            The location in the stream from which to start getting events. 0 is the beginning of time. 'now' will
            return no events and just current stream position.
        :param stream_type:
            (optional) Which type of events to return.

            NOTE: Currently, the Box API requires this to be one of the user
            events stream types. The request will fail if an enterprise events
            stream type is passed.
        :returns:
            Events corresponding to changes on Box in realtime, as they come in.
        """
        event_ids = LRUCache()
        stream_position = stream_position if stream_position is not None else self.get_latest_stream_position(stream_type=stream_type)
        while True:
            options = self.get_long_poll_options(stream_type=stream_type)
            while True:
                try:
                    long_poll_response = self.long_poll(options, stream_position)
                except Timeout:
                    break

                message = long_poll_response.json()['message']
                if message == 'new_change':
                    next_stream_position = stream_position
                    for event, next_stream_position in self._get_all_events_since(stream_position, stream_type=stream_type):
                        try:
                            event_ids.get(event['event_id'])
                        except KeyError:
                            yield event
                            event_ids.set(event['event_id'])
                    stream_position = next_stream_position
                    break
                if message == 'reconnect':
                    continue
                break

    @api_call
    def get_long_poll_options(self, stream_type: EventsStreamType = UserEventsStreamType.ALL) -> dict:
        """
        Get the url and retry timeout for setting up a long polling connection.

        :param stream_type:
            (optional) Which type of events to return.
        :returns:
            A `dict` including a long poll url, retry timeout, etc.
            E.g.
                {
                    "type": "realtime_server",
                    "url": "http://2.realtime.services.box.net/subscribe?channel=cc807c9c4869ffb1c81a&stream_type=all",
                    "ttl": "10",
                    "max_retries": "10",
                    "retry_timeout": 610,
                }
        """
        url = self.get_url()
        params = {'stream_type': stream_type}
        box_response = self._session.options(url, params=params)
        return box_response.json()['entries'][0]
