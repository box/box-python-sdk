# coding: utf-8

from __future__ import unicode_literals

from threading import Event, Thread

import pytest
import requests

from boxsdk.object.folder import FolderSyncState


@pytest.fixture
def box_events(box_client):
    return box_client.events()


@pytest.fixture
def move_target(box_client):
    return box_client.folder('0').create_subfolder('move target')


@pytest.fixture
def copy_target(box_client):
    return box_client.folder('0').create_subfolder('copy target')


@pytest.fixture
def assert_event(box_events):
    # pylint:disable=redefined-outer-name
    def helper(get_item, event_type, stream_position=0):
        item = get_item()
        events = box_events.get_events(stream_position=stream_position)['entries']
        assert len(events) == 1
        event = events[0]
        assert event['event_type'] == event_type
        assert event['source']['name'] == item.name
        assert event['source']['id'] == item.id

    return helper


def test_get_long_poll_url(box_client):
    options = box_client.events().get_long_poll_options()
    with pytest.raises(requests.Timeout):
        requests.get(options['url'], timeout=0.11)


def test_upload_causes_upload_event(uploaded_file, assert_event):
    # pylint:disable=redefined-outer-name
    assert_event(lambda: uploaded_file, 'ITEM_UPLOAD')


def test_create_folder_causes_create_event(created_subfolder, assert_event):
    # pylint:disable=redefined-outer-name
    assert_event(lambda: created_subfolder, 'ITEM_CREATE')


def test_move_file_causes_move_event(box_events, move_target, uploaded_file, assert_event):
    # pylint:disable=redefined-outer-name
    assert_event(lambda: uploaded_file.move(move_target), 'ITEM_MOVE', box_events.get_latest_stream_position())


def test_move_folder_causes_move_event(box_events, move_target, created_subfolder, assert_event):
    # pylint:disable=redefined-outer-name
    assert_event(lambda: created_subfolder.move(move_target), 'ITEM_MOVE', box_events.get_latest_stream_position())


def test_rename_file_causes_rename_event(box_events, uploaded_file, assert_event):
    # pylint:disable=redefined-outer-name
    updated_name = 'updated_{0}'.format(uploaded_file.name)
    assert_event(lambda: uploaded_file.rename(updated_name), 'ITEM_RENAME', box_events.get_latest_stream_position())


def test_rename_folder_causes_rename_event(box_events, created_subfolder, assert_event):
    # pylint:disable=redefined-outer-name
    updated_name = 'updated_{0}'.format(created_subfolder.name)
    assert_event(lambda: created_subfolder.rename(updated_name), 'ITEM_RENAME', box_events.get_latest_stream_position())


def test_copy_file_causes_copy_event(box_events, copy_target, uploaded_file, assert_event):
    # pylint:disable=redefined-outer-name
    assert_event(lambda: uploaded_file.copy(copy_target), 'ITEM_COPY', box_events.get_latest_stream_position())


def test_copy_folder_causes_copy_event(box_events, copy_target, created_subfolder, assert_event):
    # pylint:disable=redefined-outer-name
    assert_event(lambda: created_subfolder.copy(copy_target), 'ITEM_COPY', box_events.get_latest_stream_position())


@pytest.mark.xfail(reason='trash event has no source')
def test_delete_file_causes_trash_event(box_events, uploaded_file, assert_event):
    # pylint:disable=redefined-outer-name
    assert_event(uploaded_file.delete, 'ITEM_TRASH', box_events.get_latest_stream_position())


@pytest.mark.xfail(reason='trash event has no source')
def test_delete_folder_causes_trash_event(box_events, created_subfolder, assert_event):
    # pylint:disable=redefined-outer-name
    assert_event(created_subfolder.delete, 'ITEM_TRASH', box_events.get_latest_stream_position())


@pytest.mark.parametrize('sync_state,event_type', [
    (FolderSyncState.IS_SYNCED, 'ITEM_SYNC'),
    (FolderSyncState.NOT_SYNCED, 'ITEM_UNSYNC'),
])
def test_sync_folder_causes_sync_event(box_events, created_subfolder, assert_event, sync_state, event_type):
    # pylint:disable=redefined-outer-name
    assert_event(
        lambda: created_subfolder.update_sync_state(sync_state.value),
        event_type,
        box_events.get_latest_stream_position(),
    )


@pytest.fixture
def long_poll_generator(box_events, uploaded_file, request):
    # pylint:disable=redefined-outer-name
    generator = box_events.generate_events_with_long_polling(stream_position=0)

    def long_poll():
        for event in generator:
            long_poll_thread.events.append(event)
            long_poll_thread.event_ready.set()
            if long_poll_thread.should_stop_polling:
                return
            long_poll_thread.consumed_events.wait()
            long_poll_thread.consumed_events.clear()

    long_poll_thread = Thread(target=long_poll)

    long_poll_thread.should_stop_polling = False
    long_poll_thread.events = []
    long_poll_thread.event_ready = Event()
    long_poll_thread.consumed_events = Event()
    long_poll_thread.start()

    def fin():
        long_poll_thread.should_stop_polling = True
        uploaded_file.delete()
        long_poll_thread.event_ready.wait()
        generator.close()
        long_poll_thread.join()

    request.addfinalizer(fin)

    return long_poll_thread


def test_generate_events_with_long_polling(long_poll_generator, created_subfolder, uploaded_file):
    # pylint:disable=redefined-outer-name
    long_poll_generator.event_ready.wait()
    long_poll_generator.event_ready.clear()
    long_poll_generator.consumed_events.set()
    long_poll_generator.event_ready.wait()
    long_poll_generator.event_ready.clear()
    long_poll_generator.consumed_events.set()
    assert not long_poll_generator.event_ready.wait(timeout=0.01)

    assert len(long_poll_generator.events) == 2
    folder_event = next(e for e in long_poll_generator.events if e['source']['type'] == 'folder')
    file_event = next(e for e in long_poll_generator.events if e['source']['type'] == 'file')
    assert folder_event['event_type'] == 'ITEM_CREATE'
    assert file_event['event_type'] == 'ITEM_UPLOAD'
    assert folder_event['source']['id'] == created_subfolder.id
    assert file_event['source']['id'] == uploaded_file.id
    assert folder_event['source']['name'] == created_subfolder.name
    assert file_event['source']['name'] == uploaded_file.name

    del long_poll_generator.events[:]

    uploaded_file.rename('updated_{0}'.format(uploaded_file.name))
    created_subfolder.rename('updated_{0}'.format(created_subfolder.name))

    long_poll_generator.event_ready.wait()
    long_poll_generator.event_ready.clear()
    long_poll_generator.consumed_events.set()
    long_poll_generator.event_ready.wait()
    long_poll_generator.event_ready.clear()
    long_poll_generator.consumed_events.set()
    assert not long_poll_generator.event_ready.wait(timeout=0.01)

    assert len(long_poll_generator.events) == 2
    folder_event = next(e for e in long_poll_generator.events if e['source']['type'] == 'folder')
    file_event = next(e for e in long_poll_generator.events if e['source']['type'] == 'file')
    assert folder_event['event_type'] == 'ITEM_RENAME'
    assert file_event['event_type'] == 'ITEM_RENAME'
    assert folder_event['source']['id'] == created_subfolder.id
    assert file_event['source']['id'] == uploaded_file.id
    assert folder_event['source']['name'] == 'updated_{0}'.format(created_subfolder.name)
    assert file_event['source']['name'] == 'updated_{0}'.format(uploaded_file.name)
