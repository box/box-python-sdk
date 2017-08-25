# coding: utf-8

from __future__ import absolute_import, unicode_literals

import os

from betamax import Betamax
import pytest
import requests

from boxsdk import Client
from boxsdk.network.default_network import RequestsSessionNetwork
from boxsdk.session.box_session import BoxSession


# pylint:disable=redefined-outer-name


@pytest.fixture
def real_requests_session():
    return requests.Session()


@pytest.fixture(scope='module')
def betamax_cassette_library_dir(request):
    """Each directory test/foo/bar that uses betamax has a directory test/foo/bar/cassettes to hold cassettes."""
    return os.path.join(request.fspath.dirname, 'cassettes')


@pytest.fixture
def configure_betamax(betamax_cassette_library_dir):
    if not os.path.exists(betamax_cassette_library_dir):
        os.makedirs(betamax_cassette_library_dir)
    with Betamax.configure() as config:
        config.cassette_library_dir = betamax_cassette_library_dir
        config.default_cassette_options['re_record_interval'] = 100
        config.default_cassette_options['record'] = 'none' if os.environ.get('IS_CI') else 'once'


@pytest.fixture
def betamax_cassette_name(request):
    """The betamax cassette name to use for the test.

    The name is the same as the pytest nodeid (e.g.
    module_path::parametrized_test_name or
    module_path::class_name::parametrized_test_name), but replacing the full
    module-path with just the base filename, e.g. test_foo::test_bar[0].
    """
    node_ids = request.node.nodeid.split('::')
    node_ids[0] = request.fspath.purebasename
    return '::'.join(node_ids)


@pytest.fixture(scope='module')
def betamax_use_cassette_kwargs():
    return {}


@pytest.fixture
def betamax_recorder(configure_betamax, real_requests_session):   # pylint:disable=unused-argument
    return Betamax(real_requests_session)


@pytest.fixture
def betamax_cassette_recorder(betamax_recorder, betamax_cassette_name, betamax_use_cassette_kwargs):
    """Including this fixture causes the test to use a betamax cassette for network requests."""
    with betamax_recorder.use_cassette(betamax_cassette_name, **betamax_use_cassette_kwargs) as cassette_recorder:
        yield cassette_recorder


@pytest.fixture
def betamax_session(betamax_cassette_recorder):
    """A betamax-enabled requests.Session instance."""
    return betamax_cassette_recorder.session


@pytest.fixture
def betamax_boxsdk_network(betamax_session):
    """A betamax-enabled boxsdk.Network instance."""
    return RequestsSessionNetwork(session=betamax_session)


@pytest.fixture
def betamax_boxsdk_session(betamax_boxsdk_network, betamax_boxsdk_auth):
    """A betamax-enabled boxsdk.BoxSession instance.

    Requires an implementation of the abstract `betamax_boxsdk_auth` fixture,
    of type `boxsdk.OAuth2`.
    """
    return BoxSession(oauth=betamax_boxsdk_auth, network_layer=betamax_boxsdk_network)


@pytest.fixture
def betamax_boxsdk_client(betamax_boxsdk_session, betamax_boxsdk_auth):
    """A betamax-enabled boxsdk.Client instance.

    Requires an implementation of the abstract `betamax_boxsdk_auth` fixture,
    of type `boxsdk.OAuth2`.
    """
    return Client(oauth=betamax_boxsdk_auth, session=betamax_boxsdk_session)
