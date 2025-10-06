from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.events import Events

from box_sdk_gen.schemas.event import Event

from box_sdk_gen.managers.events import GetEventsStreamType

from box_sdk_gen.managers.events import GetEventsEventType

from box_sdk_gen.schemas.realtime_servers import RealtimeServers

from box_sdk_gen.schemas.realtime_server import RealtimeServer

from box_sdk_gen.internal.utils import DateTime

from box_sdk_gen.box.event_stream import EventStream

from test.box_sdk_gen.test.commons import get_default_client

from box_sdk_gen.schemas.event_source import EventSource

from box_sdk_gen.schemas.file import File

from box_sdk_gen.schemas.folder import Folder

from box_sdk_gen.schemas.user import User

from box_sdk_gen.internal.utils import date_time_from_string

from box_sdk_gen.internal.utils import get_epoch_time_in_seconds

from box_sdk_gen.internal.utils import epoch_seconds_to_date_time

client: BoxClient = get_default_client()


def testEvents():
    events: Events = client.events.get_events()
    assert len(events.entries) > 0
    first_event: Event = events.entries[0]
    assert to_string(first_event.created_by.type) == 'user'
    assert not to_string(first_event.event_type) == ''


def testEventUpload():
    events: Events = client.events.get_events(
        stream_type=GetEventsStreamType.ADMIN_LOGS,
        event_type=[GetEventsEventType.UPLOAD],
    )
    assert len(events.entries) > 0
    first_event: Event = events.entries[0]
    assert to_string(first_event.event_type) == 'UPLOAD'
    assert not to_string(first_event.additional_details.get('service_id')) == ''
    source: EventSource = first_event.source
    assert (
        to_string(source.item_type) == 'file' or to_string(source.item_type) == 'folder'
    )
    assert not source.item_id == ''
    assert not source.item_name == ''


def testEventDeleteUser():
    events: Events = client.events.get_events(
        stream_type=GetEventsStreamType.ADMIN_LOGS,
        event_type=[GetEventsEventType.DELETE_USER],
    )
    assert len(events.entries) > 0
    first_event: Event = events.entries[0]
    assert to_string(first_event.event_type) == 'DELETE_USER'
    source: User = first_event.source
    assert to_string(source.type) == 'user'
    assert not source.id == ''


def testEventSourceFileOrFolder():
    events: Events = client.events.get_events(stream_type=GetEventsStreamType.CHANGES)
    assert len(events.entries) > 0


def testGetEventsWithLongPolling():
    servers: RealtimeServers = client.events.get_events_with_long_polling()
    assert len(servers.entries) > 0
    server: RealtimeServer = servers.entries[0]
    assert to_string(server.type) == 'realtime_server'
    assert not server.url == ''


def testGetEventsWithDateFilters():
    current_epoch_time_in_seconds: int = get_epoch_time_in_seconds()
    epoch_time_in_seconds_a_week_ago: int = current_epoch_time_in_seconds - (
        ((7 * 24) * 60) * 60
    )
    created_after_date: DateTime = epoch_seconds_to_date_time(
        epoch_time_in_seconds_a_week_ago
    )
    created_before_date: DateTime = epoch_seconds_to_date_time(
        current_epoch_time_in_seconds
    )
    servers: Events = client.events.get_events(
        stream_type=GetEventsStreamType.ADMIN_LOGS,
        limit=1,
        created_after=created_after_date,
        created_before=created_before_date,
    )
    assert len(servers.entries) == 1


def testGetEventStream():
    event_stream: EventStream = client.events.get_event_stream()
    assert not event_stream == None
