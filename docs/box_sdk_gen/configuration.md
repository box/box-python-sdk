# Configuration

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Max retry attempts](#max-retry-attempts)
- [Custom retry strategy](#custom-retry-strategy)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Max retry attempts

The default maximum number of retries in case of failed API call is 5.
To change this number you should initialize `BoxRetryStrategy` with the new value and pass it to `NetworkSession`.

```python
from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth, NetworkSession, BoxRetryStrategy

auth = BoxDeveloperTokenAuth(token='DEVELOPER_TOKEN_GOES_HERE')
network_session = NetworkSession(retry_strategy=BoxRetryStrategy(max_attempts=6))
client = BoxClient(auth=auth, network_session=network_session)
```

## Custom retry strategy

You can also implement your own retry strategy by subclassing `RetryStrategy` and overriding `should_retry` and `retry_after` methods.
This example shows how to set custom strategy that retries on 5xx status codes and waits 1 second between retries.

```python
from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth, NetworkSession, RetryStrategy, FetchOptions, FetchResponse

class CustomRetryStrategy(RetryStrategy):
    def should_retry(self, fetch_options: FetchOptions, fetch_response: FetchResponse, attempt_number: int) -> bool:
        return fetch_response.status_code >= 500
    def retry_after(self, fetch_options: FetchOptions, fetch_response: FetchResponse, attempt_number: int) -> float:
        return 1.0

auth = BoxDeveloperTokenAuth(token='DEVELOPER_TOKEN_GOES_HERE')
network_session = NetworkSession(retry_strategy=CustomRetryStrategy())
client = BoxClient(auth=auth, network_session=network_session)
```
