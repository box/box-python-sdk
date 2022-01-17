Events
======

It is possible to poll the Box API for events, in order to get information about activity within Box as it happens.

The Box API supports two types of event streams: one for the events specific to a particular user and one for all of
the events in an enterprise.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [User Events](#user-events)
  - [Listening to the Event Stream](#listening-to-the-event-stream)
  - [Get the Current Stream Position](#get-the-current-stream-position)
  - [Get Events Manually](#get-events-manually)
- [Enterprise Events](#enterprise-events)
  - [Get Events Manually](#get-events-manually-1)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

User Events
-----------

The Box API provides an events endpoint that utilizes long-polling to send events in real-time. The SDK provides a
generator that automatically handles long-polling and deduplicating events.

### Listening to the Event Stream

To automatically receive events as they happen, call
[`events.generate_events_with_long_polling(stream_position=None, stream_type=UserEventsStreamType.ALL)`][generator] and iterate over
the results.  By default, this will start listening for events from the current time onward; to get all available events,
pass a `stream_position` of `0`.  The generator yields [`Event`][event_class] objects representing each event.

<!-- sample options_events -->
```python
events = client.events().generate_events_with_long_polling()
for event in events:
    print(f'Got {event.event_type} event')
```

[generator]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.events.Events.generate_events_with_long_polling
[event_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.event.Event

### Get the Current Stream Position

It is possible to get the current stream position, which can later be used to fetch events from that point in time
forward, by calling [`events.get_latest_stream_position(stream_type=UserEventsStreamType.ALL)`][get_stream_position].
This method returns the current stream position value as an `int`.

```python
stream_position = client.events().get_latest_stream_position()
print(f'The current stream position is {stream_position}')
```

[get_stream_position]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.events.Events.get_latest_stream_position

### Get Events Manually

To manually retrieve a set of events, call
[`events.get_events(limit=100, stream_position=0, stream_type=UserEventsStreamType.ALL)`][get_events].  By default, this
will fetch the first available events chronologically; you can pass a specific `stream_position` to get events from a
particular time.  This method returns a `dict` with the relevant [`Event`][event_class] objects in a `list` under the
`entries` key and the next stream position value under the `next_stream_position` key.

<!-- sample get_events -->
```python
stream_position = 0
events = client.events().get_events(stream_position=stream_position)
stream_position = events['next_stream_position']
for event in events['entries']:
    print(f'Got {event.event_type} event that occurred at {event.created_at}')
```

[get_events]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.events.Events.get_events

Enterprise Events
-----------------

Currently, the SDK only provides a manual interface for retrieving Enterprise (or Admin) Events.

### Get Events Manually

To manually retrieve a set of admin events, call
[`events.get_events(limit=100, stream_position=0, stream_type=UserEventsStreamType.ALL)`][get_events] with `stream_type`
set to `EnterpriseEventsStreamType.ADMIN_LOGS`.  By default, this will fetch the first available events chronologically;
you can pass a specific `stream_position` to get events from a particular time.  This method returns a `dict` with the
relevant [`Event`][event_class] objects in a `list` under the `entries` key and the next stream position value under the
`next_stream_position` key.

```python
from boxsdk.object.events import EnterpriseEventsStreamType

stream_position = 0
events = client.events().get_events(stream_type=EnterpriseEventsStreamType.ADMIN_LOGS, stream_position=stream_position)
stream_position = events['next_stream_position']
for event in events['entries']:
    print(f'Got {event.event_type} event that occurred at {event.created_at}')
```

### Get Admin Events

The SDK also allows you to retrieve enterprise events. Use [`events.get_admin_events_streaming(self, limit=None, stream_position=0, event_types=None)`] for live monitoring (events up to two weeks, low latency) and [`events.get_admin_events(self, limit=None, stream_position=0, created_after=None, created_before=None, event_types=None)`] for historical querying (events up to one year, higher latency).

Live monitoring example

<!-- sample get_events enterprise_stream -->
```python
 events = client.events()
    .get_admin_events_streaming()
 for event in events['entries']:
    print(f'Got {event.event_type} event that occurred at {event.created_at}') 
```

Addditionally, a list of event types can be passed along to filter down the returned events.

<!-- sample get_events enterprise_stream_filter -->
```python
 events = client.events()
    .get_admin_events_streaming(event_types=['ITEM_CREATE'])
 for event in events['entries']:
    print(f'Got {event.event_type} event that occurred at {event.created_at}') 
```

When using historical querying you can specify before and after a certain datetime and the types of events to retrieve with the `event_type` by calling
[`events.get_admin_events(self, limit=None, stream_position=0, created_after=None, created_before=None, event_types=None)`][admin_events_details].
The format for the `created_after` and `created_before` fields are supported by [RFC 3339](https://www.ietf.org/rfc/rfc3339.txt) and look
something like this: 2019-08-12T09:12:36-00:00. For more information on the date format please see [here](https://developer.box.com/en/guides/api-calls/types-and-formats/#date-and-times).
This method returns a `dict` with the relevant [`Event`][event_class] objects in a `list` under the
`entries` key and the next stream position value under the `next_stream_position` key.

<!-- sample get_events enterprise -->
```python
 events = client.events()
    .get_admin_events(created_after='2019-07-01T22:02:24-07:00')
 for event in events['entries']:
    print(f'Got {event.event_type} event that occurred at {event.created_at}') 
```

Addditionally, a list of event types can be passed along to filter down the returned events.

<!-- sample get_events enterprise_filter -->
```python
 events = client.events()
    .get_admin_events(created_after='2019-07-01T22:02:24-07:00', event_types=['ITEM_CREATE'])
 for event in events['entries']:
    print(f'Got {event.event_type} event that occurred at {event.created_at}') 
```

[admin_events_details]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.events.Events.get_admin_events
