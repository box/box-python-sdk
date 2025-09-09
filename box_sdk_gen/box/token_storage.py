import shelve
from abc import abstractmethod
from typing import Optional

from ..schemas.access_token import AccessToken


class TokenStorage:
    @abstractmethod
    def store(self, token: AccessToken) -> None:
        pass

    @abstractmethod
    def get(self) -> Optional[AccessToken]:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass


class InMemoryTokenStorage(TokenStorage):
    def __init__(self, token: Optional[AccessToken] = None):
        self._token = token

    def store(self, token: AccessToken) -> None:
        self._token = token

    def get(self) -> Optional[AccessToken]:
        return self._token

    def clear(self) -> None:
        self._token = None


class FileTokenStorage(TokenStorage):
    def __init__(self, filename: str = 'token_storage'):
        self.filename = filename

    def store(self, token: AccessToken) -> None:
        with shelve.open(self.filename) as file:
            file['token'] = token

    def get(self) -> Optional[AccessToken]:
        with shelve.open(self.filename) as file:
            return file.get('token', None)

    def clear(self) -> None:
        with shelve.open(self.filename) as file:
            if 'token' in file:
                del file['token']


class FileWithInMemoryCacheTokenStorage(TokenStorage):
    def __init__(self, filename: str = 'token_storage'):
        self.filename = filename
        self.cached_token: Optional[AccessToken] = None

    def store(self, token: AccessToken) -> None:
        with shelve.open(self.filename) as file:
            file['token'] = token
        self.cached_token = token

    def get(self) -> Optional[AccessToken]:
        if self.cached_token is None:
            with shelve.open(self.filename) as file:
                self.cached_token = file.get('token', None)
        return self.cached_token

    def clear(self) -> None:
        with shelve.open(self.filename) as file:
            if 'token' in file:
                del file['token']
        self.cached_token = None
