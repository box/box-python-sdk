# coding: utf-8

from __future__ import unicode_literals
import pytest
from boxsdk.client import Client
from boxsdk.exception import BoxAPIException


def test_create_folder_then_update_info(created_subfolder):
    # pylint:disable=redefined-outer-name
    _test_create_then_update_info(created_subfolder)


def test_create_file_then_update_info(uploaded_file):
    # pylint:disable=redefined-outer-name
    _test_create_then_update_info(uploaded_file)


def _test_create_then_update_info(item):
    updated_name = 'updated_{0}'.format(item.name)
    updated_item = item.update_info({'name': updated_name})
    assert updated_item.name == updated_name
    assert item.get().name == updated_name


def test_create_folder_then_rename(created_subfolder):
    # pylint:disable=redefined-outer-name
    _test_create_then_rename(created_subfolder)


def test_create_file_then_rename(uploaded_file):
    # pylint:disable=redefined-outer-name
    _test_create_then_rename(uploaded_file)


def _test_create_then_rename(item):
    updated_name = 'updated_{0}'.format(item.name)
    updated_item = item.rename(updated_name)
    assert updated_item.name == updated_name
    assert item.get().name == updated_name


def test_create_folder_then_move(box_client, created_subfolder):
    # pylint:disable=redefined-outer-name
    _test_create_then_move(box_client, created_subfolder)


def test_create_file_then_move(box_client, uploaded_file):
    # pylint:disable=redefined-outer-name
    _test_create_then_move(box_client, uploaded_file)


def _test_create_then_move(box_client, item):
    item_name = item.name
    move_target = box_client.folder('0').create_subfolder('move target')
    item.move(move_target)
    item = item.get()
    assert item.name == item_name
    assert item.parent['id'] == move_target.object_id
    assert len(box_client.folder('0').get_items(10)) == 1
    assert len(move_target.get_items(10)) == 1


def test_create_folder_then_copy(box_client, created_subfolder):
    # pylint:disable=redefined-outer-name
    _test_create_then_copy(box_client, created_subfolder)


def test_create_file_then_copy(box_client, uploaded_file):
    # pylint:disable=redefined-outer-name
    _test_create_then_copy(box_client, uploaded_file)


def _test_create_then_copy(box_client, item):
    # pylint:disable=redefined-outer-name
    copy_target = box_client.folder('0').create_subfolder('copy target')
    copied_item = item.copy(copy_target)
    item = item.get()
    copied_item = copied_item.get()
    assert item.id != copied_item.id
    assert item.name == copied_item.name
    assert copied_item.parent['id'] == copy_target.object_id
    assert len(box_client.folder('0').get_items(10)) == 2
    assert len(copy_target.get_items(10)) == 1


@pytest.mark.parametrize('constructor', [Client.file, Client.folder])
def test_get_item_info_for_missing_item(box_client, constructor):
    with pytest.raises(BoxAPIException) as exc_info:
        constructor(box_client, '1').get()
    assert exc_info.value.status == 404


@pytest.mark.parametrize('sync_state', ['synced', 'not_synced'])
def test_set_sync_state(created_subfolder, sync_state):
    # pylint:disable=redefined-outer-name
    folder_with_info = created_subfolder.get(fields='sync_state')
    created_subfolder.update_sync_state(sync_state)
    updated_folder_with_info = created_subfolder.get(fields='sync_state')
    assert folder_with_info.sync_state == 'not_synced'
    assert updated_folder_with_info.sync_state == sync_state
