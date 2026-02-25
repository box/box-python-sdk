from typing import Optional


class TimeoutConfig:
    def __init__(
        self,
        *,
        connection_timeout_ms: Optional[int] = None,
        read_timeout_ms: Optional[int] = None
    ):
        self.connection_timeout_ms = connection_timeout_ms
        self.read_timeout_ms = read_timeout_ms
