# coding: utf-8
import pytest
from boxsdk.object.folder import FolderSyncState


@pytest.fixture()
def extra_network_parameters():
    return {'timeout': 1}


def test_folder_clone_during_create_subfolder(created_subfolder, extra_network_parameters):
    # pylint:disable=redefined-outer-name
    # pylint:disable=protected-access
    original_folder = created_subfolder
    original_folder_id = original_folder._object_id
    original_folder_response_object = original_folder._response_object
    original_session = original_folder._session
    returned_folder = original_folder.create_subfolder('subfolder', extra_network_parameters=extra_network_parameters)
    returned_session = returned_folder._session

    assert original_session is not returned_session
    assert original_session._default_network_request_kwargs == {}
    assert returned_session._default_network_request_kwargs == {'timeout': 1}
    assert original_folder._object_id == original_folder_id
    assert original_folder._response_object == original_folder_response_object


def test_folder_clone_during_update_sync_state(created_subfolder, extra_network_parameters):
    # pylint:disable=redefined-outer-name
    # pylint:disable=protected-access
    original_folder = created_subfolder
    original_folder_id = original_folder._object_id
    original_folder_response_object = original_folder._response_object
    original_session = original_folder._session
    returned_folder = original_folder.update_sync_state(FolderSyncState.IS_SYNCED, extra_network_parameters=extra_network_parameters)
    returned_session = returned_folder._session

    assert original_session is not returned_session
    assert original_session._default_network_request_kwargs == {}
    assert returned_session._default_network_request_kwargs == {'timeout': 1}
    assert original_folder._object_id == original_folder_id
    assert original_folder._response_object == original_folder_response_object
