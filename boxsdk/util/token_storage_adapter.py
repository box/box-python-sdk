"""
Token storage adapter to bridge legacy OAuth2 token storage to generated SDK TokenStorage.

This module provides adapters that allow legacy SDK token storage mechanisms
(callbacks, in-memory storage) to work with the generated SDK's TokenStorage interface.
"""

from typing import Optional, Callable, Tuple
from box_sdk_gen.box.token_storage import TokenStorage
from box_sdk_gen.schemas.access_token import AccessToken


class LegacyTokenStorageAdapter(TokenStorage):
    """
    Adapter that bridges legacy OAuth2 token storage (callbacks) to generated SDK TokenStorage.

    This adapter wraps legacy token storage mechanisms (store_tokens callback and
    _get_tokens method) to provide a TokenStorage interface for the generated SDK.
    """

    def __init__(
        self,
        get_tokens: Callable[[], Tuple[Optional[str], Optional[str]]],
        store_tokens: Optional[Callable[[Optional[str], Optional[str]], None]] = None,
    ):
        """
        Initialize the adapter with legacy token storage callbacks.

        :param get_tokens:
            Callable that returns (access_token, refresh_token) tuple.
            This can be a method from OAuth2._get_tokens or a custom callback.
        :param store_tokens:
            Optional callable that stores tokens. Takes (access_token, refresh_token).
            If None, tokens will only be read from get_tokens but not persisted.
        """
        self._get_tokens = get_tokens
        self._store_tokens = store_tokens

    def store(self, token: AccessToken) -> None:
        """
        Store a token using the legacy storage mechanism.

        :param token:
            AccessToken object from generated SDK.
        """
        if self._store_tokens is not None:
            refresh_token = (
                token.refresh_token if hasattr(token, 'refresh_token') else None
            )
            self._store_tokens(token.access_token, refresh_token)

    def get(self) -> Optional[AccessToken]:
        """
        Get the current token from legacy storage.

        :return:
            AccessToken object if tokens are available, None otherwise.
        """
        access_token, refresh_token = self._get_tokens()

        if access_token is None:
            return None

        # Convert legacy token format to generated SDK AccessToken
        # The generated SDK AccessToken has: access_token, refresh_token, expires_in, token_type
        # We don't have expires_in from legacy, so we'll set a default or calculate if possible
        expires_in = 3600  # Default to 1 hour if not available

        return AccessToken(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
            token_type='bearer',
        )

    def clear(self) -> None:
        """
        Clear stored tokens using the legacy storage mechanism.

        Note: This will call store_tokens with None values if the callback supports it.
        """
        if self._store_tokens is not None:
            self._store_tokens(None, None)
