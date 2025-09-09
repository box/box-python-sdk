from typing import Optional


class ProxyConfig:
    def __init__(
        self,
        url: str,
        *,
        username: Optional[str] = None,
        password: Optional[str] = None
    ):
        self.url = url
        self.username = username
        self.password = password
