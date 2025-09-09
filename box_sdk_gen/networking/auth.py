from typing import Optional

from abc import abstractmethod

from typing import List

from box_sdk_gen.schemas.access_token import AccessToken

from box_sdk_gen.networking.network import NetworkSession


class Authentication:
    def __init__(self):
        pass

    @abstractmethod
    def retrieve_token(
        self, *, network_session: Optional[NetworkSession] = None
    ) -> AccessToken:
        pass

    @abstractmethod
    def refresh_token(
        self, *, network_session: Optional[NetworkSession] = None
    ) -> AccessToken:
        pass

    @abstractmethod
    def retrieve_authorization_header(
        self, *, network_session: Optional[NetworkSession] = None
    ) -> str:
        pass

    @abstractmethod
    def revoke_token(self, *, network_session: Optional[NetworkSession] = None) -> None:
        pass

    @abstractmethod
    def downscope_token(
        self,
        scopes: List[str],
        *,
        resource: Optional[str] = None,
        shared_link: Optional[str] = None,
        network_session: Optional[NetworkSession] = None
    ) -> AccessToken:
        pass
