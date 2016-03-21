# coding: utf-8

from __future__ import unicode_literals
import json
from mock import Mock, MagicMock
import pytest
from boxsdk.auth.oauth2 import DefaultNetwork
from boxsdk.network import default_network
from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.session.box_session import BoxResponse, BoxSession


@pytest.fixture()
def mock_box_session():
    mock_session = MagicMock(BoxSession)
    mock_session.get_url.side_effect = lambda *args, **kwargs: BoxSession.get_url(mock_session, *args, **kwargs)
    return mock_session


@pytest.fixture(scope='function')
def mock_network_layer():
    mock_network = Mock(DefaultNetwork)
    return mock_network


@pytest.fixture(autouse=True)
def prevent_tests_from_making_real_network_requests(monkeypatch):
    monkeypatch.delattr(default_network.requests.Session, 'request')


@pytest.fixture(scope='function')
def mock_user_response(mock_user_id, make_mock_box_request):
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        response={'type': 'user', 'id': mock_user_id},
    )
    return mock_box_response


@pytest.fixture(scope='function')
def mock_group_response(mock_group_id, make_mock_box_request):
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        response={'type': 'group', 'id': mock_group_id},
    )
    return mock_box_response


@pytest.fixture()
def make_mock_box_request():
    def inner(status_code=200, response_ok=True, response=None, content=None):
        mock_box_response = Mock(BoxResponse)
        mock_network_response = Mock(DefaultNetworkResponse)
        mock_box_response.network_response = mock_network_response
        mock_box_response.status_code = status_code
        mock_box_response.ok = response_ok
        if response is not None:
            mock_box_response.json.return_value = response
            mock_box_response.content = json.dumps(response).encode()
        else:
            mock_box_response.content = content
        return mock_box_response, mock_network_response
    return inner


@pytest.fixture(scope='function')
def mock_file_response(mock_object_id, make_mock_box_request):
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        response={'type': 'file', 'id': mock_object_id},
    )
    return mock_box_response


@pytest.fixture(scope='function')
def mock_folder_response(mock_object_id, make_mock_box_request):
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        response={'type': 'folder', 'id': mock_object_id},
    )
    return mock_box_response
