# coding: utf-8

from mock import Mock
import pytest

from boxsdk import Client
from boxsdk.auth.oauth2 import OAuth2
from boxsdk.session.session import Session, AuthorizedSession

from .mock_network import MockNetwork


@pytest.fixture()
def box_client(box_oauth, mock_box_session):
    # pylint:disable=redefined-outer-name
    return Client(box_oauth, session=mock_box_session)


@pytest.fixture()
def box_oauth(unauthorized_session, client_id, client_secret, access_token, refresh_token):
    # pylint:disable=redefined-outer-name
    return OAuth2(
        client_id,
        client_secret,
        session=unauthorized_session,
        access_token=access_token,
        refresh_token=refresh_token,
    )


@pytest.fixture()
def mock_box_network():
    return MockNetwork()


@pytest.fixture()
def unauthorized_session(mock_box_network):
    return Session(network_layer=mock_box_network)


@pytest.fixture()
def mock_box_session(mock_box_network, box_oauth):
    return AuthorizedSession(box_oauth, network_layer=mock_box_network)


@pytest.fixture
def generic_successful_response(generic_successful_request_response):
    generic_successful_request_response.request = Mock()
    return generic_successful_request_response


@pytest.fixture
def successful_token_mock(successful_token_request_response):
    successful_token_request_response.request = Mock()
    return successful_token_request_response
