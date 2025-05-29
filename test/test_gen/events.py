from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.events import Events

from box_sdk_gen.schemas.event import Event

from box_sdk_gen.managers.events import GetEventsStreamType

from box_sdk_gen.managers.events import GetEventsEventType

from box_sdk_gen.schemas.realtime_servers import RealtimeServers

from box_sdk_gen.schemas.realtime_server import RealtimeServer

from box_sdk_gen.internal.utils import DateTime

from test.commons import get_default_client

from box_sdk_gen.schemas.event_source import EventSource

from box_sdk_gen.schemas.file import File

from box_sdk_gen.schemas.folder import Folder

from box_sdk_gen.schemas.user import User

from box_sdk_gen.internal.utils import date_time_from_string

client: BoxClient = get_default_client()

def testEvents():
    events: Events = client.events.get_events()
    assert len(events.entries) > 0
    first_event: Event = events.entries[0]
    assert to_string(first_event.created_by.type) == 'user'
    assert not to_string(first_event.event_type) == ''

def testEventUpload():
    events: Events = client.events.get_events(stream_type=GetEventsStreamType.ADMIN_LOGS, event_type=[GetEventsEventType.UPLOAD])
    assert len(events.entries) > 0
    first_event: Event = events.entries[0]
    assert to_string(first_event.event_type) == 'UPLOAD'
    source: EventSource = first_event.source
    assert to_string(source.item_type) == 'file' or to_string(source.item_type) == 'folder'
    assert not source.item_id == ''
    assert not source.item_name == ''

def testEventDeleteUser():
    events: Events = client.events.get_events(stream_type=GetEventsStreamType.ADMIN_LOGS, event_type=[GetEventsEventType.DELETE_USER])
    assert len(events.entries) > 0
    first_event: Event = events.entries[0]
    assert to_string(first_event.event_type) == 'DELETE_USER'
    source: User = first_event.source
    assert to_string(source.type) == 'user'
    assert not source.id == ''

def testEventSourceFileOrFolder():
    events: Events = client.events.get_events(stream_type=GetEventsStreamType.CHANGES)
    assert len(events.entries) > 0
    first_event: Event = events.entries[0]
    source: File = first_event.source
    assert (to_string(source.type) == 'file' or to_string(source.type) == 'folder') or to_string(source.type) == 'collaboration'
    assert not source.id == ''

def testGetEventsWithLongPolling():
    servers: RealtimeServers = client.events.get_events_with_long_polling()
    assert len(servers.entries) > 0
    server: RealtimeServer = servers.entries[0]
    assert to_string(server.type) == 'realtime_server'
    assert not server.url == ''

def testGetEventsWithDateFilters():
    created_after_date: DateTime = date_time_from_string('2024-06-09T00:00:00Z')
    created_before_date: DateTime = date_time_from_string('2025-06-09T00:00:00Z')
    servers: Events = client.events.get_events(stream_type=GetEventsStreamType.ADMIN_LOGS, limit=1, created_after=created_after_date, created_before=created_before_date)
    assert len(servers.entries) == 1