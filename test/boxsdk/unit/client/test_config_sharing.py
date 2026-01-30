"""
Unit tests for configuration sharing methods in Client class.

Tests get_sdk_gen_authentication(), get_sdk_gen_network_session(), and get_sdk_gen_client() methods.
"""

from unittest.mock import Mock
import pytest

from boxsdk.client import Client
from boxsdk.auth.developer_token_auth import DeveloperTokenAuth
from boxsdk.auth.oauth2 import OAuth2
from boxsdk.auth.jwt_auth import JWTAuth
from boxsdk.auth.ccg_auth import CCGAuth
from boxsdk.config import API, Proxy
from box_sdk_gen.box.developer_token_auth import BoxDeveloperTokenAuth
from box_sdk_gen.box.oauth import BoxOAuth
from box_sdk_gen.box.jwt_auth import BoxJWTAuth
from box_sdk_gen.box.ccg_auth import BoxCCGAuth
from box_sdk_gen.networking.network import NetworkSession
from box_sdk_gen.networking.base_urls import BaseUrls
from box_sdk_gen.client import BoxClient


class TestGetSdkGenAuthentication:
    """Test cases for get_sdk_gen_authentication() method."""

    def test_get_authentication_developer_token(self, mock_box_session):
        """Test converting DeveloperTokenAuth to BoxDeveloperTokenAuth."""
        token = 'dev_token_123'
        auth = DeveloperTokenAuth(get_new_token_callback=lambda: token)

        client = Client(auth, session=mock_box_session)
        gen_auth = client.get_sdk_gen_authentication()

        assert isinstance(gen_auth, BoxDeveloperTokenAuth)
        assert gen_auth.token == token

    def test_get_authentication_developer_token_missing_token(self, mock_box_session):
        """Test that missing developer token raises ValueError."""
        # Create auth with callback that returns None
        auth = DeveloperTokenAuth(get_new_token_callback=lambda: None)
        auth._access_token = None

        client = Client(auth, session=mock_box_session)

        with pytest.raises(ValueError, match="Developer token is not available"):
            client.get_sdk_gen_authentication()

    def test_get_authentication_oauth2(self, mock_box_session):
        """Test converting OAuth2 to BoxOAuth."""
        client_id = 'test_client_id'
        client_secret = 'test_client_secret'
        access_token = 'test_access_token'
        refresh_token = 'test_refresh_token'

        auth = OAuth2(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            refresh_token=refresh_token,
        )

        client = Client(auth, session=mock_box_session)
        gen_auth = client.get_sdk_gen_authentication()

        assert isinstance(gen_auth, BoxOAuth)
        assert gen_auth.config.client_id == client_id
        assert gen_auth.config.client_secret == client_secret

    def test_get_authentication_oauth2_missing_credentials(self, mock_box_session):
        """Test that missing OAuth2 credentials raises ValueError."""
        auth = OAuth2(client_id=None, client_secret=None)

        client = Client(auth, session=mock_box_session)

        with pytest.raises(
            ValueError, match="OAuth2 client_id and client_secret are required"
        ):
            client.get_sdk_gen_authentication()

    def test_get_authentication_oauth2_with_custom_token_storage(
        self, mock_box_session
    ):
        """Test OAuth2 conversion with custom token storage."""
        from box_sdk_gen.box.token_storage import InMemoryTokenStorage

        auth = OAuth2(
            client_id='test_id',
            client_secret='test_secret',
            access_token='token',
            refresh_token='refresh',
        )

        custom_storage = InMemoryTokenStorage()
        client = Client(auth, session=mock_box_session)
        gen_auth = client.get_sdk_gen_authentication(token_storage=custom_storage)

        assert isinstance(gen_auth, BoxOAuth)
        assert gen_auth.config.token_storage is custom_storage

    def test_get_authentication_jwt(self, mock_box_session):
        """Test converting JWTAuth to BoxJWTAuth."""
        from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
        from cryptography.hazmat.primitives import serialization as crypto_serialization

        # Create a mock RSA private key
        mock_key = Mock(spec=RSAPrivateKey)
        mock_key.private_bytes.return_value = (
            b'-----BEGIN PRIVATE KEY-----\nMOCK_KEY\n-----END PRIVATE KEY-----'
        )

        client_id = 'test_client_id'
        client_secret = 'test_client_secret'
        jwt_key_id = 'test_key_id'
        enterprise_id = 'test_enterprise_id'

        auth = JWTAuth(
            client_id=client_id,
            client_secret=client_secret,
            enterprise_id=enterprise_id,
            jwt_key_id=jwt_key_id,
            rsa_private_key_data=mock_key,
        )

        client = Client(auth, session=mock_box_session)
        gen_auth = client.get_sdk_gen_authentication()

        assert isinstance(gen_auth, BoxJWTAuth)
        assert gen_auth.config.client_id == client_id
        assert gen_auth.config.client_secret == client_secret
        assert gen_auth.config.jwt_key_id == jwt_key_id
        assert gen_auth.config.enterprise_id == enterprise_id

    def test_get_authentication_jwt_missing_credentials(self, mock_box_session):
        """Test that missing JWT credentials raises ValueError."""
        from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

        # Create a mock RSA private key
        mock_key = Mock(spec=RSAPrivateKey)
        mock_key.private_bytes.return_value = (
            b'-----BEGIN PRIVATE KEY-----\nMOCK_KEY\n-----END PRIVATE KEY-----'
        )

        # Create auth with missing client_id
        auth = JWTAuth(
            client_id=None,  # Missing required field
            client_secret='test_secret',
            enterprise_id='test_enterprise',
            jwt_key_id='test_key_id',
            rsa_private_key_data=mock_key,
        )

        client = Client(auth, session=mock_box_session)

        with pytest.raises(ValueError, match="JWT authentication requires"):
            client.get_sdk_gen_authentication()

    def test_get_authentication_ccg(self, mock_box_session):
        """Test converting CCGAuth to BoxCCGAuth."""
        client_id = 'test_client_id'
        client_secret = 'test_client_secret'
        enterprise_id = 'test_enterprise_id'

        auth = CCGAuth(
            client_id=client_id,
            client_secret=client_secret,
            enterprise_id=enterprise_id,
        )

        client = Client(auth, session=mock_box_session)
        gen_auth = client.get_sdk_gen_authentication()

        assert isinstance(gen_auth, BoxCCGAuth)
        assert gen_auth.config.client_id == client_id
        assert gen_auth.config.client_secret == client_secret
        assert gen_auth.config.enterprise_id == enterprise_id

    def test_get_authentication_ccg_missing_credentials(self, mock_box_session):
        """Test that missing CCG credentials raises ValueError."""
        auth = CCGAuth(client_id=None, client_secret=None)

        client = Client(auth, session=mock_box_session)

        with pytest.raises(ValueError, match="CCG authentication requires"):
            client.get_sdk_gen_authentication()

    def test_get_authentication_unsupported_type(self, mock_box_session):
        """Test that unsupported auth type raises ValueError."""
        # Create a mock auth that's not one of the supported types
        mock_auth = Mock()
        mock_auth.__class__.__name__ = 'UnsupportedAuth'

        client = Client(mock_auth, session=mock_box_session)

        with pytest.raises(ValueError, match="Unsupported authentication type"):
            client.get_sdk_gen_authentication()


class TestGetSdkGenNetworkSession:
    """Test cases for get_sdk_gen_network_session() method."""

    def test_get_network_session_default(self, mock_box_session):
        """Test extracting network session with default settings."""
        auth = Mock(OAuth2)
        client = Client(auth, session=mock_box_session)

        network_session = client.get_sdk_gen_network_session()

        assert isinstance(network_session, NetworkSession)
        assert isinstance(network_session.base_urls, BaseUrls)

    def test_get_network_session_with_custom_headers(self, mock_box_session):
        """Test network session with custom headers."""
        auth = Mock(OAuth2)
        client = Client(auth, session=mock_box_session)

        additional_headers = {'X-Custom-Header': 'custom_value'}
        network_session = client.get_sdk_gen_network_session(
            additional_headers=additional_headers
        )

        assert 'X-Custom-Header' in network_session.additional_headers
        assert network_session.additional_headers['X-Custom-Header'] == 'custom_value'

    def test_get_network_session_with_proxy(self, mock_box_session):
        """Test network session with proxy configuration."""
        # Set up proxy config
        Proxy.URL = 'http://proxy.example.com:8080'
        Proxy.AUTH = None

        auth = Mock(OAuth2)
        client = Client(auth, session=mock_box_session)

        network_session = client.get_sdk_gen_network_session()

        # Proxy URL should be set
        assert network_session.proxy_url is not None
        assert 'proxy.example.com' in network_session.proxy_url

        # Clean up
        Proxy.URL = None

    def test_get_network_session_with_authenticated_proxy(self, mock_box_session):
        """Test network session with authenticated proxy."""
        # Set up authenticated proxy config
        Proxy.URL = 'http://proxy.example.com:8080'
        Proxy.AUTH = {'user': 'proxy_user', 'password': 'proxy_pass'}

        auth = Mock(OAuth2)
        client = Client(auth, session=mock_box_session)

        network_session = client.get_sdk_gen_network_session()

        # Proxy URL should include authentication
        assert network_session.proxy_url is not None
        assert 'proxy_user' in network_session.proxy_url
        assert 'proxy_pass' in network_session.proxy_url

        # Clean up
        Proxy.URL = None
        Proxy.AUTH = None

    def test_get_network_session_with_custom_retry_strategy(self, mock_box_session):
        """Test network session with custom retry strategy."""
        from box_sdk_gen.networking.retries import BoxRetryStrategy

        auth = Mock(OAuth2)
        client = Client(auth, session=mock_box_session)

        custom_retry = BoxRetryStrategy(max_attempts=10, retry_base_interval=2.0)
        network_session = client.get_sdk_gen_network_session(retry_strategy=custom_retry)

        assert network_session.retry_strategy is custom_retry
        assert network_session.retry_strategy.max_attempts == 10

    def test_get_network_session_base_urls(self, mock_box_session):
        """Test that base URLs are correctly extracted."""
        # Modify API config
        original_base_url = API.BASE_API_URL
        original_upload_url = API.UPLOAD_URL

        API.BASE_API_URL = 'https://custom.api.box.com/2.0'
        API.UPLOAD_URL = 'https://custom.upload.box.com/api/2.0'

        auth = Mock(OAuth2)
        client = Client(auth, session=mock_box_session)

        network_session = client.get_sdk_gen_network_session()

        # URLs should have version suffix removed
        assert 'custom.api.box.com' in network_session.base_urls.base_url
        assert 'custom.upload.box.com' in network_session.base_urls.upload_url

        # Restore
        API.BASE_API_URL = original_base_url
        API.UPLOAD_URL = original_upload_url


class TestGetSdkGenClient:
    """Test cases for get_sdk_gen_client() method."""

    def test_get_sdk_gen_client_basic(self, mock_box_session):
        """Test basic usage of get_sdk_gen_client()."""
        token = 'dev_token'
        auth = DeveloperTokenAuth(get_new_token_callback=lambda: token)

        client = Client(auth, session=mock_box_session)
        gen_client = client.get_sdk_gen_client()

        assert isinstance(gen_client, BoxClient)
        assert isinstance(gen_client.auth, BoxDeveloperTokenAuth)
        assert gen_client.auth.token == token

    def test_get_sdk_gen_client_oauth2(self, mock_box_session):
        """Test get_sdk_gen_client() with OAuth2."""
        auth = OAuth2(
            client_id='test_id',
            client_secret='test_secret',
            access_token='token',
            refresh_token='refresh',
        )

        client = Client(auth, session=mock_box_session)
        gen_client = client.get_sdk_gen_client()

        assert isinstance(gen_client, BoxClient)
        assert isinstance(gen_client.auth, BoxOAuth)

    def test_get_sdk_gen_client_with_auth_options(self, mock_box_session):
        """Test get_sdk_gen_client() with custom auth options."""
        from box_sdk_gen.box.token_storage import InMemoryTokenStorage

        auth = OAuth2(
            client_id='test_id',
            client_secret='test_secret',
            access_token='token',
            refresh_token='refresh',
        )

        custom_storage = InMemoryTokenStorage()
        client = Client(auth, session=mock_box_session)
        gen_client = client.get_sdk_gen_client(
            auth_options={'token_storage': custom_storage}
        )

        assert isinstance(gen_client, BoxClient)
        assert gen_client.auth.config.token_storage is custom_storage

    def test_get_sdk_gen_client_with_network_options(self, mock_box_session):
        """Test get_sdk_gen_client() with custom network options."""
        from box_sdk_gen.networking.retries import BoxRetryStrategy

        token = 'dev_token'
        auth = DeveloperTokenAuth(get_new_token_callback=lambda: token)

        custom_retry = BoxRetryStrategy(max_attempts=10)
        client = Client(auth, session=mock_box_session)
        gen_client = client.get_sdk_gen_client(
            network_options={'retry_strategy': custom_retry}
        )

        assert isinstance(gen_client, BoxClient)
        assert gen_client.network_session.retry_strategy.max_attempts == 10

    def test_get_sdk_gen_client_with_all_options(self, mock_box_session):
        """Test get_sdk_gen_client() with both auth and network options."""
        from box_sdk_gen.box.token_storage import InMemoryTokenStorage
        from box_sdk_gen.networking.retries import BoxRetryStrategy

        auth = OAuth2(
            client_id='test_id',
            client_secret='test_secret',
            access_token='token',
            refresh_token='refresh',
        )

        custom_storage = InMemoryTokenStorage()
        custom_retry = BoxRetryStrategy(max_attempts=15)
        additional_headers = {'X-Test': 'value'}

        client = Client(auth, session=mock_box_session)
        gen_client = client.get_sdk_gen_client(
            auth_options={'token_storage': custom_storage},
            network_options={
                'retry_strategy': custom_retry,
                'additional_headers': additional_headers,
            },
        )

        assert isinstance(gen_client, BoxClient)
        assert gen_client.auth.config.token_storage is custom_storage
        assert gen_client.network_session.retry_strategy.max_attempts == 15
        assert gen_client.network_session.additional_headers['X-Test'] == 'value'
