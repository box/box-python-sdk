from abc import abstractmethod

from typing import Optional

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import random


class RetryStrategy:
    def __init__(self):
        pass

    @abstractmethod
    def should_retry(
        self,
        fetch_options: FetchOptions,
        fetch_response: FetchResponse,
        attempt_number: int,
    ) -> bool:
        pass

    @abstractmethod
    def retry_after(
        self,
        fetch_options: FetchOptions,
        fetch_response: FetchResponse,
        attempt_number: int,
    ) -> float:
        pass


class BoxRetryStrategy(RetryStrategy):
    def __init__(
        self,
        *,
        max_attempts: int = 5,
        retry_randomization_factor: float = 0.5,
        retry_base_interval: float = 1,
        max_retries_on_exception: int = 2,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.max_attempts = max_attempts
        self.retry_randomization_factor = retry_randomization_factor
        self.retry_base_interval = retry_base_interval
        self.max_retries_on_exception = max_retries_on_exception

    def should_retry(
        self,
        fetch_options: FetchOptions,
        fetch_response: FetchResponse,
        attempt_number: int,
    ) -> bool:
        if fetch_response.status == 0:
            return attempt_number <= self.max_retries_on_exception
        is_successful: bool = (
            fetch_response.status >= 200 and fetch_response.status < 400
        )
        retry_after_header: Optional[str] = (
            fetch_response.headers.get('Retry-After')
            if 'Retry-After' in fetch_response.headers
            else None
        )
        is_accepted_with_retry_after: bool = (
            fetch_response.status == 202 and not retry_after_header == None
        )
        if attempt_number >= self.max_attempts:
            return False
        if is_accepted_with_retry_after:
            return True
        if fetch_response.status >= 500:
            return True
        if fetch_response.status == 429:
            return True
        if fetch_response.status == 401 and not fetch_options.auth == None:
            fetch_options.auth.refresh_token(
                network_session=fetch_options.network_session
            )
            return True
        if is_successful:
            return False
        return False

    def retry_after(
        self,
        fetch_options: FetchOptions,
        fetch_response: FetchResponse,
        attempt_number: int,
    ) -> float:
        retry_after_header: Optional[str] = fetch_response.headers.get('Retry-After')
        if not retry_after_header == None:
            return float(retry_after_header)
        randomization: float = random(
            1 - self.retry_randomization_factor, 1 + self.retry_randomization_factor
        )
        exponential: float = 2**attempt_number
        return (exponential * self.retry_base_interval) * randomization
