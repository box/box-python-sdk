# coding: utf-8

from __future__ import unicode_literals
from mock import Mock
import pytest
from boxsdk.auth.oauth2 import DefaultNetwork
from boxsdk.network import default_network
from boxsdk.session.box_session import BoxSession


@pytest.fixture()
def mock_box_session():
    return Mock(BoxSession)


@pytest.fixture(scope='function')
def mock_network_layer():
    mock_network = Mock(DefaultNetwork)
    return mock_network


@pytest.fixture(autouse=True)
def prevent_tests_from_making_real_network_requests(monkeypatch):
    monkeypatch.delattr(default_network.requests.Session, 'request')
