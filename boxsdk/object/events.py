# coding: utf-8

from __future__ import unicode_literals

from requests.exceptions import Timeout
from six import with_metaclass

from boxsdk.object.base_endpoint import BaseEndpoint
from boxsdk.util.enum import ExtendableEnumMeta
from boxsdk.util.lru_cache import LRUCache
from boxsdk.util.text_enum import TextEnum


# pylint:disable=too-many-ancestors
class EventsStreamType(with_metaclass(ExtendableEnumMeta, TextEnum)):
    """An enum of all possible values of the `stream_type` parameter for user events.

    The value of the `stream_type` parameter determines the type of events
    returned by the endpoint.

    <https://box-content.readme.io/reference#events>
    """


class UserEventsStreamType(EventsStreamType):
    """An enum of all possible values of the `stream_type` parameter for user events.

    - ALL: Returns all user events.
    - CHANGES: Returns tree changes.
    - SYNC: Returns tree changes only for sync folders.

    <https://box-content.readme.io/reference#standard-user-events>
    """
    ALL = 'all'
    CHANGES = 'changes'
    SYNC = 'sync'


class EnterpriseEventsStreamType(EventsStreamType):
    """An enum of all possible values of the `stream_type` parameter for enterprise events.

    - ADMIN_LOGS: Retrieves up to a year's events for all users in the enterprise.

    NOTE: Requires Admin: These stream types will only work with an auth token
    from an enterprise admin account.

    <https://box-content.readme.io/reference#enterprise-events>
    """
    ADMIN_LOGS = 'admin_logs'
# pylint:enable=too-many-ancestors


class Events(BaseEndpoint):
    """Box API endpoint for subscribing to changes in a Box account."""

    def get_url(self, *args):
        """Base class override."""
        return super(Events, self).get_url('events', *args)

    def get_events(self, limit=100, stream_position=0, stream_type=UserEventsStreamType.ALL):
        """
        Get Box events from a given stream position for a given stream type.

        :param limit:
            Maximum number of events to return.
        :type limit:
            `int`
        :param stream_position:
            The location in the stream from which to start getting events. 0 is the beginning of time. 'now' will
            return no events and just current stream position.

            NOTE: Currently, 'now' is only valid for user events stream types. The request will fail if an
            enterprise events stream type is passed.
        :type stream_position:
            `unicode`
        :param stream_type:
            (optional) Which type of events to return.
            Defaults to `UserEventsStreamType.ALL`.
        :type stream_type:
            :enum:`EventsStreamType`
        :returns:
            JSON response from the Box /events endpoint. Contains the next stream position to use for the next call,
            along with some number of events.
        :rtype:
            `dict`
        """
        url = self.get_url()
        params = {
            'limit': limit,
            'stream_position': stream_position,
            'stream_type': stream_type,
        }
        box_response = self._session.get(url, params=params)
        return box_response.json()

    def get_latest_stream_position(self, stream_type=UserEventsStreamType.ALL):
        """
        Get the latest stream position. The return value can be used with :meth:`get_events` or
        :meth:`generate_events_with_long_polling`.

        :param stream_type:
            (optional) Which events stream to query.
            Defaults to `UserEventsStreamType.ALL`.

            NOTE: Currently, the Box API requires this to be one of the user
            events stream types. The request will fail if an enterprise events
            stream type is passed.
        :type stream_type:
            :enum:`UserEventsStreamType`
        :returns:
            The latest stream position.
        :rtype:
            `unicode`
        """
        return self.get_events(limit=0, stream_position='now', stream_type=stream_type)['next_stream_position']

    def _get_all_events_since(self, stream_position, stream_type=UserEventsStreamType.ALL):
        """
        :param stream_type:
            (optional) Which type of events to return.
            Defaults to `UserEventsStreamType.ALL`.
        :type stream_type:
            :enum:`EventsStreamType`
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

    def long_poll(self, options, stream_position):
        """
        Set up a long poll connection at the specified url.

        :param options:
            The long poll options which include a long pull url, retry timeout, etc.
        :type options:
            `dict`
        :param stream_position:
            The location in the stream from which to start getting events. 0 is the beginning of time.
            'now' will return no events and just current stream position.
        :type stream_position:
            `unicode`
        :returns:
            {"message": "new_change"}, which means there're new changes on Box or {"version": 1, "message": "reconnect"}
            if nothing happens on Box during the long poll.
        :rtype:
            `dict`
        """
        url = options['url']
        long_poll_response = self._session.get(
            url,
            timeout=options['retry_timeout'],
            params={'stream_position': stream_position}
        )
        return long_poll_response

    def generate_events_with_long_polling(self, stream_position=None, stream_type=UserEventsStreamType.ALL):
        """
        Subscribe to events from the given stream position.

        :param stream_position:
            The location in the stream from which to start getting events. 0 is the beginning of time. 'now' will
            return no events and just current stream position.
        :type stream_position:
            `unicode`
        :param stream_type:
            (optional) Which type of events to return.
            Defaults to `UserEventsStreamType.ALL`.

            NOTE: Currently, the Box API requires this to be one of the user
            events stream types. The request will fail if an enterprise events
            stream type is passed.
        :type stream_type:
            :enum:`UserEventsStreamType`
        :returns:
            Events corresponding to changes on Box in realtime, as they come in.
        :rtype:
            `generator` of :class:`Event`
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
                else:
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
                    elif message == 'reconnect':
                        continue
                    else:
                        break

    def get_long_poll_options(self, stream_type=UserEventsStreamType.ALL):
        """
        Get the url and retry timeout for setting up a long polling connection.

        :param stream_type:
            (optional) Which type of events to return.
            Defaults to `UserEventsStreamType.ALL`.
        :type stream_type:
            :enum:`EventsStreamType`
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
        :rtype:
            `dict`
        """
        url = self.get_url()
        params = {'stream_type': stream_type}
        box_response = self._session.options(url, params=params)
        return box_response.json()['entries'][0]
