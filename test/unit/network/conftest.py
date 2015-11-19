# coding: utf-8

from __future__ import unicode_literals
from mock import Mock
import pytest
from requests import Session


@pytest.fixture()
def mock_request(monkeypatch):
    mock_session_factory = Mock()
    mock_session_factory.return_value = session = Mock(Session, request=Mock())
    monkeypatch.setattr('requests.Session', mock_session_factory)
    return session.request


@pytest.fixture(params=('GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'))
def http_verb(request):
    return request.param
