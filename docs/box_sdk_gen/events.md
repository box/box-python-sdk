# EventsManager

- [Get events long poll endpoint](#get-events-long-poll-endpoint)
- [List user and enterprise events](#list-user-and-enterprise-events)
- [Get event stream](#get-event-stream)

## Get events long poll endpoint

Returns a list of real-time servers that can be used for long-polling updates
to the [event stream](https://developer.box.com/reference/get-events).

Long polling is the concept where a HTTP request is kept open until the
server sends a response, then repeating the process over and over to receive
updated responses.

Long polling the event stream can only be used for user events, not for
enterprise events.

To use long polling, first use this endpoint to retrieve a list of long poll
URLs. Next, make a long poll request to any of the provided URLs.

When an event occurs in monitored account a response with the value
`new_change` will be sent. The response contains no other details as
it only serves as a prompt to take further action such as sending a
request to the [events endpoint](https://developer.box.com/reference/get-events) with the last known
`stream_position`.

After the server sends this response it closes the connection. You must now
repeat the long poll process to begin listening for events again.

If no events occur for a while and the connection times out you will
receive a response with the value `reconnect`. When you receive this response
you’ll make another call to this endpoint to restart the process.

If you receive no events in `retry_timeout` seconds then you will need to
make another request to the real-time server (one of the URLs in the response
for this endpoint). This might be necessary due to network errors.

Finally, if you receive a `max_retries` error when making a request to the
real-time server, you should start over by making a call to this endpoint
first.

This operation is performed by calling function `get_events_with_long_polling`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/options-events/).

<!-- sample options_events -->

```python
client.events.get_events_with_long_polling()
```

### Arguments

- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `RealtimeServers`.

Returns a paginated array of servers that can be used
instead of the regular endpoints for long-polling events.

## List user and enterprise events

Returns up to a year of past events for a given user
or for the entire enterprise.

By default this returns events for the authenticated user. To retrieve events
for the entire enterprise, set the `stream_type` to `admin_logs_streaming`
for live monitoring of new events, or `admin_logs` for querying across
historical events. The user making the API call will
need to have admin privileges, and the application will need to have the
scope `manage enterprise properties` checked.

This operation is performed by calling function `get_events`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-events/).

<!-- sample get_events -->

```python
client.events.get_events()
```

### Arguments

- stream_type `Optional[GetEventsStreamType]`
  - Defines the type of events that are returned _ `all` returns everything for a user and is the default _ `changes` returns events that may cause file tree changes such as file updates or collaborations. _ `sync` is similar to `changes` but only applies to synced folders _ `admin_logs` returns all events for an entire enterprise and requires the user making the API call to have admin permissions. This stream type is for programmatically pulling from a 1 year history of events across all users within the enterprise and within a `created_after` and `created_before` time frame. The complete history of events will be returned in chronological order based on the event time, but latency will be much higher than `admin_logs_streaming`. \* `admin_logs_streaming` returns all events for an entire enterprise and requires the user making the API call to have admin permissions. This stream type is for polling for recent events across all users within the enterprise. Latency will be much lower than `admin_logs`, but events will not be returned in chronological order and may contain duplicates.
- stream_position `Optional[str]`
  - The location in the event stream to start receiving events from. _ `now` will return an empty list events and the latest stream position for initialization. _ `0` or `null` will return all events.
- limit `Optional[int]`
  - Limits the number of events returned. Note: Sometimes, the events less than the limit requested can be returned even when there may be more events remaining. This is primarily done in the case where a number of events have already been retrieved and these retrieved events are returned rather than delaying for an unknown amount of time to see if there are any more results.
- event_type `Optional[List[GetEventsEventType]]`
  - A comma-separated list of events to filter by. This can only be used when requesting the events with a `stream_type` of `admin_logs` or `adming_logs_streaming`. For any other `stream_type` this value will be ignored.
- created_after `Optional[DateTime]`
  - The lower bound date and time to return events for. This can only be used when requesting the events with a `stream_type` of `admin_logs`. For any other `stream_type` this value will be ignored.
- created_before `Optional[DateTime]`
  - The upper bound date and time to return events for. This can only be used when requesting the events with a `stream_type` of `admin_logs`. For any other `stream_type` this value will be ignored.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Events`.

Returns a list of event objects.

Events objects are returned in pages, with each page (chunk)
including a list of event objects. The response includes a
`chunk_size` parameter indicating how many events were returned in this
chunk, as well as the next `stream_position` that can be
queried.

## Get event stream

Get an event stream for the Box API

This operation is performed by calling function `get_event_stream`.

```python
client.events.get_event_stream()
```

### Arguments

- query_params `GetEventStreamQueryParams`
  - Query parameters of getEvents method
- headers `GetEventStreamHeaders`
  - Headers of getEvents method

### Returns

This function returns a value of type `EventStream`.
