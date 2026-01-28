"""
Helpers for sharing configuration between legacy `boxsdk` and generated `box_sdk_gen`.

This module keeps the conversion logic out of `boxsdk.client.client.Client` so the
Client class can delegate to a smaller surface area.
"""

from __future__ import annotations

from typing import Optional, Any, Dict

from boxsdk.auth.ccg_auth import CCGAuth
from boxsdk.auth.developer_token_auth import DeveloperTokenAuth
from boxsdk.auth.jwt_auth import JWTAuth
from boxsdk.auth.oauth2 import OAuth2 as LegacyOAuth2
from boxsdk.util.token_storage_adapter import LegacyTokenStorageAdapter

from box_sdk_gen.box.ccg_auth import BoxCCGAuth, CCGConfig
from box_sdk_gen.box.developer_token_auth import BoxDeveloperTokenAuth
from box_sdk_gen.box.jwt_auth import BoxJWTAuth, JWTConfig
from box_sdk_gen.box.oauth import BoxOAuth, OAuthConfig
from box_sdk_gen.box.token_storage import TokenStorage
from box_sdk_gen.client import BoxClient
from box_sdk_gen.networking.auth import Authentication
from box_sdk_gen.networking.base_urls import BaseUrls
from box_sdk_gen.networking.network import NetworkSession
from box_sdk_gen.networking.retries import BoxRetryStrategy
from box_sdk_gen.schemas.access_token import AccessToken


def get_authentication(
    legacy_client: Any, *, token_storage: Optional[TokenStorage] = None
) -> Authentication:
    oauth = legacy_client._oauth  # pylint: disable=protected-access

    if isinstance(oauth, DeveloperTokenAuth):
        return _get_authentication_for_developer_token(oauth)

    if _is_oauth2_authentication(oauth):
        return _get_authentication_for_oauth2(oauth, token_storage=token_storage)

    if isinstance(oauth, JWTAuth):
        return _get_authentication_for_jwt(oauth, token_storage=token_storage)

    if isinstance(oauth, CCGAuth):
        return _get_authentication_for_ccg(oauth, token_storage=token_storage)

    raise ValueError(
        f"Unsupported authentication type: {type(oauth).__name__}. "
        "Supported types: DeveloperTokenAuth, OAuth2, JWTAuth, CCGAuth"
    )


def get_network_session(
    legacy_client: Any,
    *,
    network_client=None,
    retry_strategy=None,
    data_sanitizer=None,
    additional_headers=None,
) -> NetworkSession:
    session = legacy_client._session  # pylint: disable=protected-access
    api_config = session.api_config
    proxy_config = session.proxy_config

    base_urls = _get_base_urls(api_config)

    # Extract or create retry strategy
    if retry_strategy is None:
        max_retries = getattr(api_config, 'MAX_RETRY_ATTEMPTS', 5)
        retry_base_interval = getattr(session, '_retry_base_interval', 1.0)
        retry_strategy = BoxRetryStrategy(
            max_attempts=max_retries, retry_base_interval=retry_base_interval
        )

    # Handle proxy configuration
    proxy_url = None
    if proxy_config and hasattr(proxy_config, 'URL') and proxy_config.URL:
        proxy_url = proxy_config.URL
        if hasattr(proxy_config, 'AUTH') and proxy_config.AUTH:
            auth = proxy_config.AUTH
            if isinstance(auth, dict) and 'user' in auth and 'password' in auth:
                scheme = proxy_url.split('://', 1)[0] if '://' in proxy_url else 'http'
                host = proxy_url.split('//')[1] if '//' in proxy_url else proxy_url
                proxy_url = f"{scheme}://{auth['user']}:{auth['password']}@{host}"

    # Merge custom headers
    headers: Dict[str, str] = {}
    if hasattr(session, '_default_headers'):
        headers.update(session._default_headers.copy())
    if additional_headers:
        headers.update(additional_headers)

    return NetworkSession(
        base_urls=base_urls,
        network_client=network_client,
        retry_strategy=retry_strategy,
        additional_headers=headers if headers else None,
        proxy_url=proxy_url,
        data_sanitizer=data_sanitizer,
    )


def get_sdk_gen_client(
    legacy_client: Any,
    *,
    auth_options: Optional[dict] = None,
    network_options: Optional[dict] = None,
) -> BoxClient:
    token_storage = None
    if auth_options and 'token_storage' in auth_options:
        token_storage = auth_options['token_storage']

    auth = get_authentication(legacy_client, token_storage=token_storage)

    network_kwargs = {}
    if network_options:
        network_kwargs = {
            'network_client': network_options.get('network_client'),
            'retry_strategy': network_options.get('retry_strategy'),
            'data_sanitizer': network_options.get('data_sanitizer'),
            'additional_headers': network_options.get('additional_headers'),
        }

    network_session = get_network_session(legacy_client, **network_kwargs)
    return BoxClient(auth=auth, network_session=network_session)


def _is_oauth2_authentication(oauth: object) -> bool:
    return isinstance(oauth, LegacyOAuth2) and not isinstance(
        oauth, (DeveloperTokenAuth, JWTAuth, CCGAuth)
    )


def _get_base_urls(api_config: object) -> BaseUrls:
    """
    Convert legacy api_config URLs to generated SDK BaseUrls.

    The generated SDK expects base URLs without the `/2.0` suffix and will append
    endpoint paths itself.
    """
    base_url = getattr(api_config, 'BASE_API_URL', 'https://api.box.com/2.0')
    if base_url.endswith('/2.0'):
        base_url = base_url[:-4]
    elif base_url.endswith('/2'):
        base_url = base_url[:-2]

    upload_url = getattr(api_config, 'UPLOAD_URL', 'https://upload.box.com/api/2.0')
    if upload_url.endswith('/2.0'):
        upload_url = upload_url[:-4]
    elif upload_url.endswith('/2'):
        upload_url = upload_url[:-2]

    oauth2_url = getattr(
        api_config, 'OAUTH2_AUTHORIZE_URL', 'https://account.box.com/api/oauth2'
    )
    if '/authorize' in oauth2_url:
        oauth2_url = oauth2_url[: oauth2_url.rindex('/authorize')]

    return BaseUrls(base_url=base_url, upload_url=upload_url, oauth_2_url=oauth2_url)


def _get_default_token_storage() -> TokenStorage:
    from box_sdk_gen.box.token_storage import InMemoryTokenStorage

    return InMemoryTokenStorage()


def _get_authentication_for_developer_token(
    oauth: DeveloperTokenAuth,
) -> Authentication:
    token = oauth.access_token
    if not token:
        raise ValueError("Developer token is not available")
    return BoxDeveloperTokenAuth(token=token)


def _get_authentication_for_oauth2(
    oauth: LegacyOAuth2, *, token_storage: Optional[TokenStorage] = None
) -> Authentication:
    client_id = getattr(oauth, '_client_id', None)
    client_secret = getattr(oauth, '_client_secret', None)

    if not client_id or not client_secret:
        raise ValueError("OAuth2 client_id and client_secret are required")

    if token_storage is None:
        token_storage = LegacyTokenStorageAdapter(
            get_tokens=lambda: oauth._get_tokens(),
            store_tokens=lambda access_token, refresh_token: oauth._store_tokens(
                access_token, refresh_token
            ),
        )

    config = OAuthConfig(
        client_id=client_id,
        client_secret=client_secret,
        token_storage=token_storage,
    )
    auth = BoxOAuth(config=config)

    return auth


def _get_authentication_for_jwt(
    oauth: JWTAuth, *, token_storage: Optional[TokenStorage] = None
) -> Authentication:
    client_id = getattr(oauth, '_client_id', None)
    client_secret = getattr(oauth, '_client_secret', None)
    jwt_key_id = getattr(oauth, '_jwt_key_id', None)
    rsa_private_key = getattr(oauth, '_rsa_private_key', None)
    enterprise_id = getattr(oauth, '_enterprise_id', None)
    user_id = getattr(oauth, '_user_id', None)

    if not all([client_id, client_secret, jwt_key_id, rsa_private_key]):
        raise ValueError(
            "JWT authentication requires client_id, client_secret, jwt_key_id, and private key"
        )

    from cryptography.hazmat.primitives import serialization

    try:
        private_key_pem = rsa_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode('utf-8')
        passphrase = ''
    except Exception as e:
        raise ValueError(
            f"Cannot serialize private key: {e}. Please ensure the private key is valid."
        ) from e

    if token_storage is None:
        token_storage = _get_default_token_storage()

    config = JWTConfig(
        client_id=client_id,
        client_secret=client_secret,
        jwt_key_id=jwt_key_id,
        private_key=private_key_pem,
        private_key_passphrase=passphrase,
        enterprise_id=enterprise_id,
        user_id=user_id,
        token_storage=token_storage,
    )

    auth = BoxJWTAuth(config=config)
    return auth


def _get_authentication_for_ccg(
    oauth: CCGAuth, *, token_storage: Optional[TokenStorage] = None
) -> Authentication:
    client_id = getattr(oauth, '_client_id', None)
    client_secret = getattr(oauth, '_client_secret', None)
    enterprise_id = getattr(oauth, '_enterprise_id', None)
    user_id = getattr(oauth, '_user_id', None)

    if not client_id or not client_secret:
        raise ValueError("CCG authentication requires client_id and client_secret")

    if token_storage is None:
        token_storage = _get_default_token_storage()

    config = CCGConfig(
        client_id=client_id,
        client_secret=client_secret,
        enterprise_id=enterprise_id,
        user_id=user_id,
        token_storage=token_storage,
    )

    auth = BoxCCGAuth(config=config)
    return auth
