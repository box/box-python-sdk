import threading
from enum import Enum
from typing import Optional, Generator

from ..box.errors import BoxSDKError
from ..schemas.events import Events
from ..schemas.event import Event
from ..schemas.realtime_server import RealtimeServer
from ..networking.fetch_options import FetchOptions, ResponseFormat
from ..networking.fetch_response import FetchResponse


class RealtimeServerEvent(str, Enum):
    NEW_CHANGE = 'new_change'
    RECONNECT = 'reconnect'


class EventStreamAction(str, Enum):
    FETCH_EVENTS = 'fetch_events'
    RECONNECT = 'reconnect'
    RETRY = 'retry'
    STOP = 'stop'


class EventStream:
    """
    EventStream is an iterator that fetches events from the Box API.
    It uses long polling to receive real-time updates.
    This class is designed to be used as a Python iterator.

    Example usage:
        events_stream = client.events.get_event_stream()
        for event in events_stream:
            print(event)
    """

    def __init__(self, *, events_manager, query_params, headers_input):
        """
        Initialize the EventStream.

        :param events_manager: The EventsManager instance which provides relevant methods to fetch events.
        :param query_params: The query parameters to use for fetching events.
        :param headers_input: The headers to include in the request.
        """
        self._events_manager = events_manager
        self._query_params = query_params
        self._headers_input = headers_input
        self._stream_position = query_params.stream_position or 'now'
        self._long_polling_info: Optional[RealtimeServer] = None
        self._long_polling_retries: int = 0
        self._started: bool = False
        self._stopped: bool = False
        self._stop_event = threading.Event()
        self._deduplication_size = 1000
        self._dedupHash = dict()

    def __iter__(self) -> Generator[Event, None, None]:
        """Make EventStream iterable. Yields Event objects."""
        return self._event_generator()

    def _event_generator(self) -> Generator[Event, None, None]:
        """Generator that yields Event objects from the stream."""
        if not self._started:
            self._started = True

        try:
            # Start with fetching events to get initial events and stream position
            yield from self._fetch_events()

            # Then start long polling loop
            while not self._stopped and not self._stop_event.is_set():
                try:
                    action = self._get_long_poll_info_and_poll()

                    if action == EventStreamAction.FETCH_EVENTS:
                        # Fetch new events when notified
                        yield from self._fetch_events()
                    elif action == EventStreamAction.RECONNECT:
                        # Continue the loop to get new long polling info
                        continue
                    elif action == EventStreamAction.RETRY:
                        # Wait a bit before retrying
                        if not self._stop_event.wait(5):
                            continue
                        else:
                            break
                    elif action == EventStreamAction.STOP:
                        break
                    else:
                        # Continue long polling
                        continue

                except Exception as e:
                    if not self._stopped and not self._stop_event.is_set():
                        # Wait a bit before retrying
                        if not self._stop_event.wait(5):
                            continue
                    break

        except Exception as e:
            if not self._stopped and not self._stop_event.is_set():
                pass
            return

    def stop(self):
        """Stop the event stream."""
        self._stopped = True
        self._stop_event.set()

    def _get_long_poll_info(self):
        """Fetch long polling info from the server."""
        if self._stopped or self._stop_event.is_set():
            return

        try:
            info = self._events_manager.get_events_with_long_polling()

            server = next(
                (e for e in info.entries or [] if e.type == 'realtime_server'), None
            )
            if not server:
                raise BoxSDKError(message='No realtime server found in the response.')

            self._long_polling_info = server
            self._long_polling_retries = 0

        except Exception as error:
            if not self._stopped and not self._stop_event.is_set():
                raise error

    def _get_long_poll_info_and_poll(self) -> str:
        """Get long polling info and perform a long poll, returning the action to take."""
        if self._stopped or self._stop_event.is_set():
            return 'stop'

        # Get long polling info if needed
        if not self._long_polling_info or self._long_polling_retries > int(
            self._long_polling_info.max_retries or '10'
        ):
            self._get_long_poll_info()

        return self._do_long_poll()

    def _do_long_poll(self) -> str:
        """Perform the long polling request and return action to take."""
        if self._stopped or self._stop_event.is_set():
            return EventStreamAction.STOP

        try:
            self._long_polling_retries += 1

            long_poll_url = self._long_polling_info.url
            separator = '&' if '?' in long_poll_url else '?'
            long_poll_with_stream_position = (
                f"{long_poll_url}{separator}stream_position={self._stream_position}"
            )

            response: FetchResponse = (
                self._events_manager.network_session.network_client.fetch(
                    FetchOptions(
                        url=long_poll_with_stream_position,
                        method='GET',
                        headers={
                            'Content-Type': 'application/json',
                        },
                        response_format=ResponseFormat.JSON,
                        auth=self._events_manager.auth,
                        network_session=self._events_manager.network_session,
                    )
                )
            )

            if self._stopped or self._stop_event.is_set():
                return EventStreamAction.STOP

            if response.data:
                message = response.data

                if isinstance(message, dict):
                    message_text = message.get('message', '')

                    if message_text == RealtimeServerEvent.NEW_CHANGE:
                        return EventStreamAction.FETCH_EVENTS
                    elif message_text == RealtimeServerEvent.RECONNECT:
                        return EventStreamAction.RECONNECT

                # Continue long polling
                return self._do_long_poll()

        except Exception as error:
            if not self._stopped and not self._stop_event.is_set():
                return 'retry'

        return 'stop'

    def _fetch_events(self) -> Generator[Event, None, None]:
        """Fetch events from the API and yield Event objects."""
        if self._stopped or self._stop_event.is_set():
            return

        try:
            # Prepare query parameters for the get_events call
            fetch_params = self._query_params.__dict__
            fetch_params['stream_position'] = self._stream_position

            # Add extra headers if provided
            if self._headers_input and self._headers_input.extra_headers:
                fetch_params['extra_headers'] = self._headers_input.extra_headers

            events: Events = self._events_manager.get_events(**fetch_params)

            # Update stream position for next request
            if events.next_stream_position is not None:
                self._stream_position = str(events.next_stream_position)
            else:
                self._stream_position = 'now'

            # Yield Event objects if any
            if events.entries:
                for event in events.entries:
                    event_id = event.event_id
                    if event_id not in self._dedupHash:
                        self._dedupHash[event_id] = True
                        if self._stopped or self._stop_event.is_set():
                            return
                        yield event

            if len(self._dedupHash) > self._deduplication_size:
                self._dedupHash.clear()
                event_ids = list(events.entries.map(lambda e: e.event_id))
                for event_id in event_ids:
                    self._dedupHash[event_id] = True

        except Exception as error:
            if not self._stopped and not self._stop_event.is_set():
                raise error
