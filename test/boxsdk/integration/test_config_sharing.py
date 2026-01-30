"""
Integration tests for configuration sharing between legacy and generated SDKs.

These tests verify that configuration sharing works end-to-end with real
authentication and network configurations.
"""

from unittest.mock import Mock

from boxsdk import Client
from boxsdk.auth.developer_token_auth import DeveloperTokenAuth
from boxsdk.auth.oauth2 import OAuth2
from boxsdk.auth.jwt_auth import JWTAuth
from boxsdk.auth.ccg_auth import CCGAuth
from boxsdk.config import API, Proxy
from box_sdk_gen.client import BoxClient
from box_sdk_gen.box.developer_token_auth import BoxDeveloperTokenAuth
from box_sdk_gen.box.oauth import BoxOAuth
from box_sdk_gen.box.jwt_auth import BoxJWTAuth
from box_sdk_gen.box.ccg_auth import BoxCCGAuth
from box_sdk_gen.networking.network import NetworkSession


class TestConfigSharingIntegration:
    """Integration tests for configuration sharing."""

    def test_developer_token_roundtrip(self, mock_box_session):
        """Test that developer token auth works end-to-end."""
        token = 'test_dev_token_12345'
        legacy_auth = DeveloperTokenAuth(get_new_token_callback=lambda: token)

        legacy_client = Client(legacy_auth, session=mock_box_session)

        # Get generated client
        gen_client = legacy_client.get_sdk_gen_client()

        # Verify both clients are configured
        assert isinstance(gen_client, BoxClient)
        assert isinstance(gen_client.auth, BoxDeveloperTokenAuth)
        assert gen_client.auth.token == token

        # Verify network session is configured
        assert isinstance(gen_client.network_session, NetworkSession)

    def test_oauth2_roundtrip(self, mock_box_session):
        """Test that OAuth2 auth works end-to-end with token sharing."""
        client_id = 'test_client_id_123'
        client_secret = 'test_client_secret_456'
        access_token = 'test_access_token_789'
        refresh_token = 'test_refresh_token_012'

        legacy_auth = OAuth2(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            refresh_token=refresh_token,
        )

        legacy_client = Client(legacy_auth, session=mock_box_session)

        # Get generated client
        gen_client = legacy_client.get_sdk_gen_client()

        # Verify authentication
        assert isinstance(gen_client, BoxClient)
        assert isinstance(gen_client.auth, BoxOAuth)
        assert gen_client.auth.config.client_id == client_id
        assert gen_client.auth.config.client_secret == client_secret

        # Verify token storage is shared
        stored_token = gen_client.auth.token_storage.get()
        assert stored_token is not None
        assert stored_token.access_token == access_token
        assert stored_token.refresh_token == refresh_token

    def test_oauth2_token_synchronization(self, mock_box_session):
        """Test that tokens are synchronized between legacy and generated clients."""
        client_id = 'test_client_id'
        client_secret = 'test_client_secret'

        # Track token storage
        stored_tokens = {'access': 'initial_token', 'refresh': 'initial_refresh'}

        def get_tokens():
            return (stored_tokens.get('access'), stored_tokens.get('refresh'))

        def store_tokens(access_token, refresh_token):
            stored_tokens['access'] = access_token
            stored_tokens['refresh'] = refresh_token

        legacy_auth = OAuth2(
            client_id=client_id, client_secret=client_secret, store_tokens=store_tokens
        )
        legacy_auth._get_tokens = get_tokens
        legacy_auth._store_tokens = store_tokens

        legacy_client = Client(legacy_auth, session=mock_box_session)
        gen_client = legacy_client.get_sdk_gen_client()

        # Update token via generated client
        from box_sdk_gen.schemas.access_token import AccessToken

        new_token = AccessToken(
            access_token='new_token',
            refresh_token='new_refresh',
            expires_in=3600,
            token_type='bearer',
        )
        gen_client.auth.token_storage.store(new_token)

        # Verify legacy client sees the update
        access, refresh = legacy_auth._get_tokens()
        assert access == 'new_token'
        assert refresh == 'new_refresh'

    def test_network_configuration_preservation(self, mock_box_session):
        """Test that network configuration is preserved."""
        # Set up custom API config
        original_base_url = API.BASE_API_URL
        original_upload_url = API.UPLOAD_URL

        API.BASE_API_URL = 'https://custom.api.box.com/2.0'
        API.UPLOAD_URL = 'https://custom.upload.box.com/api/2.0'

        try:
            legacy_auth = DeveloperTokenAuth(get_new_token_callback=lambda: 'token')
            legacy_client = Client(legacy_auth, session=mock_box_session)

            gen_client = legacy_client.get_sdk_gen_client()

            # Verify base URLs are preserved
            assert 'custom.api.box.com' in gen_client.network_session.base_urls.base_url
            assert (
                'custom.upload.box.com'
                in gen_client.network_session.base_urls.upload_url
            )
        finally:
            # Restore original values
            API.BASE_API_URL = original_base_url
            API.UPLOAD_URL = original_upload_url

    def test_proxy_configuration_preservation(self, mock_box_session):
        """Test that proxy configuration is preserved."""
        # Set up proxy
        original_proxy_url = Proxy.URL
        original_proxy_auth = Proxy.AUTH

        Proxy.URL = 'http://proxy.example.com:8080'
        Proxy.AUTH = {'user': 'proxy_user', 'password': 'proxy_pass'}

        try:
            legacy_auth = DeveloperTokenAuth(get_new_token_callback=lambda: 'token')
            legacy_client = Client(legacy_auth, session=mock_box_session)

            gen_client = legacy_client.get_sdk_gen_client()

            # Verify proxy is configured
            assert gen_client.network_session.proxy_url is not None
            assert 'proxy.example.com' in gen_client.network_session.proxy_url
            assert 'proxy_user' in gen_client.network_session.proxy_url
        finally:
            # Restore original values
            Proxy.URL = original_proxy_url
            Proxy.AUTH = original_proxy_auth

    def test_custom_headers_preservation(self, mock_box_session):
        """Test that custom headers are preserved."""
        legacy_auth = DeveloperTokenAuth(get_new_token_callback=lambda: 'token')
        legacy_client = Client(legacy_auth, session=mock_box_session)

        # Add custom headers to session
        mock_box_session._default_headers = {'X-Custom-Header': 'custom_value'}

        gen_client = legacy_client.get_sdk_gen_client()

        # Verify headers are preserved
        assert 'X-Custom-Header' in gen_client.network_session.additional_headers
        assert (
            gen_client.network_session.additional_headers['X-Custom-Header']
            == 'custom_value'
        )

    def test_retry_strategy_preservation(self, mock_box_session):
        """Test that retry strategy is preserved."""
        # Modify API config
        original_max_retries = API.MAX_RETRY_ATTEMPTS
        API.MAX_RETRY_ATTEMPTS = 10

        try:
            legacy_auth = DeveloperTokenAuth(get_new_token_callback=lambda: 'token')
            legacy_client = Client(legacy_auth, session=mock_box_session)

            gen_client = legacy_client.get_sdk_gen_client()

            # Verify retry strategy
            assert gen_client.network_session.retry_strategy.max_attempts == 10
        finally:
            API.MAX_RETRY_ATTEMPTS = original_max_retries

    def test_jwt_auth_roundtrip(self, mock_box_session):
        """Test that JWT auth works end-to-end."""
        from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

        # Create a mock RSA private key
        mock_key = Mock(spec=RSAPrivateKey)
        mock_key.private_bytes.return_value = (
            b'-----BEGIN PRIVATE KEY-----\nMOCK_KEY\n-----END PRIVATE KEY-----'
        )

        client_id = 'test_jwt_client_id'
        client_secret = 'test_jwt_client_secret'
        jwt_key_id = 'test_jwt_key_id'
        enterprise_id = 'test_enterprise_id'

        legacy_auth = JWTAuth(
            client_id=client_id,
            client_secret=client_secret,
            enterprise_id=enterprise_id,
            jwt_key_id=jwt_key_id,
            rsa_private_key_data=mock_key,
        )

        legacy_client = Client(legacy_auth, session=mock_box_session)
        gen_client = legacy_client.get_sdk_gen_client()

        # Verify authentication
        assert isinstance(gen_client, BoxClient)
        assert isinstance(gen_client.auth, BoxJWTAuth)
        assert gen_client.auth.config.client_id == client_id
        assert gen_client.auth.config.client_secret == client_secret
        assert gen_client.auth.config.jwt_key_id == jwt_key_id
        assert gen_client.auth.config.enterprise_id == enterprise_id

    def test_ccg_auth_roundtrip(self, mock_box_session):
        """Test that CCG auth works end-to-end."""
        client_id = 'test_ccg_client_id'
        client_secret = 'test_ccg_client_secret'
        enterprise_id = 'test_ccg_enterprise_id'

        legacy_auth = CCGAuth(
            client_id=client_id,
            client_secret=client_secret,
            enterprise_id=enterprise_id,
        )

        legacy_client = Client(legacy_auth, session=mock_box_session)
        gen_client = legacy_client.get_sdk_gen_client()

        # Verify authentication
        assert isinstance(gen_client, BoxClient)
        assert isinstance(gen_client.auth, BoxCCGAuth)
        assert gen_client.auth.config.client_id == client_id
        assert gen_client.auth.config.client_secret == client_secret
        assert gen_client.auth.config.enterprise_id == enterprise_id

    def test_parallel_client_usage(self, mock_box_session):
        """Test that both legacy and generated clients can be used in parallel."""
        token = 'parallel_token'
        legacy_auth = DeveloperTokenAuth(get_new_token_callback=lambda: token)

        legacy_client = Client(legacy_auth, session=mock_box_session)
        gen_client = legacy_client.get_sdk_gen_client()

        # Both clients should be functional
        assert legacy_client.auth.access_token == token
        assert gen_client.auth.token == token

        # Both should have network sessions
        assert legacy_client.session is not None
        assert gen_client.network_session is not None

    def test_get_authentication_with_custom_token_storage(self, mock_box_session):
        """Test get_sdk_gen_authentication() with custom token storage."""
        from box_sdk_gen.box.token_storage import InMemoryTokenStorage

        legacy_auth = OAuth2(
            client_id='test_id',
            client_secret='test_secret',
            access_token='token',
            refresh_token='refresh',
        )

        custom_storage = InMemoryTokenStorage()
        legacy_client = Client(legacy_auth, session=mock_box_session)
        gen_auth = legacy_client.get_sdk_gen_authentication(
            token_storage=custom_storage
        )

        assert isinstance(gen_auth, BoxOAuth)
        assert gen_auth.config.token_storage is custom_storage

    def test_get_network_session_with_custom_options(self, mock_box_session):
        """Test get_sdk_gen_network_session() with custom options."""
        from box_sdk_gen.networking.retries import BoxRetryStrategy

        legacy_auth = DeveloperTokenAuth(get_new_token_callback=lambda: 'token')
        legacy_client = Client(legacy_auth, session=mock_box_session)

        custom_retry = BoxRetryStrategy(max_attempts=20, retry_base_interval=2.5)
        custom_headers = {'X-Custom': 'value'}

        network_session = legacy_client.get_sdk_gen_network_session(
            retry_strategy=custom_retry, additional_headers=custom_headers
        )

        assert network_session.retry_strategy.max_attempts == 20
        assert network_session.retry_strategy.retry_base_interval == 2.5
        assert network_session.additional_headers['X-Custom'] == 'value'

    def test_get_sdk_gen_client_with_all_options(self, mock_box_session):
        """Test get_sdk_gen_client() with all options."""
        from box_sdk_gen.box.token_storage import InMemoryTokenStorage
        from box_sdk_gen.networking.retries import BoxRetryStrategy

        legacy_auth = OAuth2(
            client_id='test_id',
            client_secret='test_secret',
            access_token='token',
            refresh_token='refresh',
        )

        custom_storage = InMemoryTokenStorage()
        custom_retry = BoxRetryStrategy(max_attempts=25)
        custom_headers = {'X-Full-Test': 'full_value'}

        legacy_client = Client(legacy_auth, session=mock_box_session)
        gen_client = legacy_client.get_sdk_gen_client(
            auth_options={'token_storage': custom_storage},
            network_options={
                'retry_strategy': custom_retry,
                'additional_headers': custom_headers,
            },
        )

        # Verify all options are applied
        assert gen_client.auth.config.token_storage is custom_storage
        assert gen_client.network_session.retry_strategy.max_attempts == 25
        assert (
            gen_client.network_session.additional_headers['X-Full-Test'] == 'full_value'
        )
