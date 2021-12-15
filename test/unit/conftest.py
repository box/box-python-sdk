# coding: utf-8

import copy
import json

from mock import Mock, MagicMock
import pytest

from boxsdk.config import API, Client, Proxy
from boxsdk.network import default_network
from boxsdk.network.default_network import DefaultNetworkResponse, DefaultNetwork
from boxsdk.session.box_response import BoxResponse
from boxsdk.session.session import Session
from boxsdk.util.translator import Translator


@pytest.fixture(scope='function', autouse=True)
def original_default_translator():
    """A reference to the default translator, before the reference is changed by `default_translator` below."""
    return Translator._default_translator   # pylint:disable=protected-access


@pytest.yield_fixture(scope='function', autouse=True)
def default_translator(original_default_translator):
    """The default translator to use during the test.

    We don't want global state to mutate across tests. So before each test
    (because of autouse=True), we make a copy of the default translator, and
    assign this copy to Translator._default_translator. At the end of the test,
    we reset the reference.
    """
    try:
        translator = Translator(dict(copy.deepcopy(original_default_translator)), extend_default_translator=False, new_child=False)
        Translator._default_translator = translator   # pylint:disable=protected-access
        yield translator
    finally:
        Translator._default_translator = original_default_translator  # pylint:disable=protected-access


@pytest.fixture(scope='function')
def translator(default_translator):   # pylint:disable=unused-argument
    return Translator(extend_default_translator=True, new_child=True)


@pytest.fixture(scope='function')
def mock_box_session(translator):
    mock_session = MagicMock(Session)
    # pylint:disable=protected-access
    mock_session._api_config = mock_session.api_config = API()
    mock_session._client_config = mock_session.client_config = Client()
    mock_session._proxy_config = mock_session.proxy_config = Proxy()
    # pylint:enable=protected-access
    mock_session.get_url.side_effect = lambda *args, **kwargs: Session.get_url(mock_session, *args, **kwargs)
    mock_session.translator = translator
    return mock_session


@pytest.fixture()
def mock_box_session_2(translator):
    mock_session = MagicMock(Session)
    # pylint:disable=protected-access
    mock_session._api_config = API()
    mock_session._client_config = Client()
    mock_session._proxy_config = Proxy()
    # pylint:enable=protected-access
    mock_session.get_url.side_effect = lambda *args, **kwargs: Session.get_url(mock_session, *args, **kwargs)
    mock_session.translator = translator
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


@pytest.fixture(scope='function')
def mock_web_link_response(mock_object_id, make_mock_box_request):
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        response={'type': 'web_link', 'id': mock_object_id},
    )
    return mock_box_response
