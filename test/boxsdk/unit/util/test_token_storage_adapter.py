"""
Unit tests for token storage adapter.

Tests the LegacyTokenStorageAdapter that bridges legacy OAuth2 token storage
to generated SDK TokenStorage interface.
"""

from unittest.mock import Mock, MagicMock
import pytest

from boxsdk.util.token_storage_adapter import LegacyTokenStorageAdapter
from box_sdk_gen.schemas.access_token import AccessToken


class TestLegacyTokenStorageAdapter:
    """Test cases for LegacyTokenStorageAdapter."""

    def test_store_with_store_callback(self):
        """Test storing tokens using the legacy store callback."""
        stored_tokens = {}

        def get_tokens():
            return (stored_tokens.get('access'), stored_tokens.get('refresh'))

        def store_tokens(access_token, refresh_token):
            stored_tokens['access'] = access_token
            stored_tokens['refresh'] = refresh_token

        adapter = LegacyTokenStorageAdapter(
            get_tokens=get_tokens, store_tokens=store_tokens
        )

        token = AccessToken(
            access_token='test_access_token',
            refresh_token='test_refresh_token',
            expires_in=3600,
            token_type='bearer',
        )

        adapter.store(token)

        assert stored_tokens['access'] == 'test_access_token'
        assert stored_tokens['refresh'] == 'test_refresh_token'

    def test_store_without_store_callback(self):
        """Test that store works even without a store callback."""

        def get_tokens():
            return (None, None)

        adapter = LegacyTokenStorageAdapter(get_tokens=get_tokens, store_tokens=None)

        token = AccessToken(
            access_token='test_access_token',
            refresh_token='test_refresh_token',
            expires_in=3600,
            token_type='bearer',
        )

        # Should not raise an error
        adapter.store(token)

    def test_get_with_tokens(self):
        """Test retrieving tokens when they exist."""

        def get_tokens():
            return ('test_access_token', 'test_refresh_token')

        adapter = LegacyTokenStorageAdapter(get_tokens=get_tokens, store_tokens=None)

        token = adapter.get()

        assert token is not None
        assert token.access_token == 'test_access_token'
        assert token.refresh_token == 'test_refresh_token'
        assert token.expires_in == 3600  # Default value
        assert token.token_type == 'bearer'

    def test_get_without_tokens(self):
        """Test retrieving tokens when they don't exist."""

        def get_tokens():
            return (None, None)

        adapter = LegacyTokenStorageAdapter(get_tokens=get_tokens, store_tokens=None)

        token = adapter.get()

        assert token is None

    def test_get_with_only_access_token(self):
        """Test retrieving when only access token is available."""

        def get_tokens():
            return ('test_access_token', None)

        adapter = LegacyTokenStorageAdapter(get_tokens=get_tokens, store_tokens=None)

        token = adapter.get()

        assert token is not None
        assert token.access_token == 'test_access_token'
        assert token.refresh_token is None

    def test_clear_with_store_callback(self):
        """Test clearing tokens using the legacy store callback."""
        stored_tokens = {'access': 'token', 'refresh': 'refresh_token'}

        def get_tokens():
            return (stored_tokens.get('access'), stored_tokens.get('refresh'))

        def store_tokens(access_token, refresh_token):
            if access_token is None:
                stored_tokens.clear()
            else:
                stored_tokens['access'] = access_token
                stored_tokens['refresh'] = refresh_token

        adapter = LegacyTokenStorageAdapter(
            get_tokens=get_tokens, store_tokens=store_tokens
        )

        adapter.clear()

        assert stored_tokens == {}

    def test_clear_without_store_callback(self):
        """Test that clear works even without a store callback."""

        def get_tokens():
            return ('token', 'refresh_token')

        adapter = LegacyTokenStorageAdapter(get_tokens=get_tokens, store_tokens=None)

        # Should not raise an error
        adapter.clear()

    def test_token_conversion_format(self):
        """Test that tokens are converted to the correct AccessToken format."""

        def get_tokens():
            return ('access_123', 'refresh_456')

        adapter = LegacyTokenStorageAdapter(get_tokens=get_tokens, store_tokens=None)

        token = adapter.get()

        assert isinstance(token, AccessToken)
        assert token.access_token == 'access_123'
        assert token.refresh_token == 'refresh_456'
        assert token.expires_in == 3600
        assert token.token_type == 'bearer'

    def test_store_and_get_roundtrip(self):
        """Test storing and retrieving tokens in a roundtrip."""
        stored_tokens = {}

        def get_tokens():
            return (stored_tokens.get('access'), stored_tokens.get('refresh'))

        def store_tokens(access_token, refresh_token):
            stored_tokens['access'] = access_token
            stored_tokens['refresh'] = refresh_token

        adapter = LegacyTokenStorageAdapter(
            get_tokens=get_tokens, store_tokens=store_tokens
        )

        # Store a token
        original_token = AccessToken(
            access_token='stored_access',
            refresh_token='stored_refresh',
            expires_in=7200,
            token_type='bearer',
        )
        adapter.store(original_token)

        # Retrieve it
        retrieved_token = adapter.get()

        assert retrieved_token is not None
        assert retrieved_token.access_token == 'stored_access'
        assert retrieved_token.refresh_token == 'stored_refresh'
