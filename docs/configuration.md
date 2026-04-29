# Configuration

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Retry Strategy](#retry-strategy)
  - [Overview](#overview)
  - [Default Configuration](#default-configuration)
  - [Retry Decision Flow](#retry-decision-flow)
  - [Exponential Backoff Algorithm](#exponential-backoff-algorithm)
    - [Example Delays (with default settings)](#example-delays-with-default-settings)
  - [Retry-After Header](#retry-after-header)
  - [Network Exception Handling](#network-exception-handling)
  - [Customizing Retry Parameters](#customizing-retry-parameters)
  - [Custom Retry Strategy](#custom-retry-strategy)
- [Timeouts](#timeouts)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Retry Strategy

### Overview

The SDK ships with a built-in retry strategy (`BoxRetryStrategy`) that implements the `RetryStrategy` interface. The `BoxNetworkClient`, which serves as the default network client, uses this strategy to automatically retry failed API requests with exponential backoff.

The retry strategy exposes two methods:

- **`should_retry`** — Determines whether a failed request should be retried based on the HTTP status code, response headers, attempt count, and authentication state.
- **`retry_after`** — Computes the delay (in seconds) before the next retry attempt, using either the server-provided `Retry-After` header or an exponential backoff formula.

### Default Configuration

| Parameter                    | Default      | Description                                                                                                                                              |
| ---------------------------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `max_attempts`               | `5`          | Maximum number of retry attempts for HTTP error responses (status 4xx/5xx).                                                                              |
| `retry_base_interval`        | `1` (second) | Base interval used in the exponential backoff calculation.                                                                                               |
| `retry_randomization_factor` | `0.5`        | Jitter factor applied to the backoff delay. The actual delay is multiplied by a random value between `1 - factor` and `1 + factor`.                      |
| `max_retries_on_exception`   | `2`          | Maximum number of retries for network-level exceptions (connection failures, timeouts). These are tracked by a separate counter from HTTP error retries. |

### Retry Decision Flow

The following diagram shows how `BoxRetryStrategy.should_retry` decides whether to retry a request:

```
                    should_retry(fetch_options, fetch_response, attempt_number)
                                        |
                                        v
                             +-----------------------+
                             | status == 0           |     Yes
                             | (network exception)?  |----------> attempt_number <= max_retries_on_exception?
                             +-----------------------+               |            |
                                        | No                        Yes          No
                                        v                            |            |
                             +-----------------------+           [RETRY]      [NO RETRY]
                             | attempt_number >=     |
                             | max_attempts?         |
                             +-----------------------+
                                  |            |
                                 Yes          No
                                  |            |
                             [NO RETRY]        v
                             +-----------------------+
                             | status == 202 AND     |     Yes
                             | Retry-After header?   |----------> [RETRY]
                             +-----------------------+
                                        | No
                                        v
                             +-----------------------+
                             | status >= 500         |     Yes
                             | (server error)?       |----------> [RETRY]
                             +-----------------------+
                                        | No
                                        v
                             +-----------------------+
                             | status == 429         |     Yes
                             | (rate limited)?       |----------> [RETRY]
                             +-----------------------+
                                        | No
                                        v
                             +-----------------------+
                             | status == 401 AND     |     Yes
                             | auth available?       |----------> Refresh token, then [RETRY]
                             +-----------------------+
                                        | No
                                        v
                                   [NO RETRY]
```

### Exponential Backoff Algorithm

When the response does not include a `Retry-After` header, the retry delay is computed using exponential backoff with randomized jitter:

```
delay = 2^attempt_number * retry_base_interval * random(1 - factor, 1 + factor)
```

Where:

- `attempt_number` is the current attempt (1-based)
- `retry_base_interval` defaults to `1` second
- `factor` is `retry_randomization_factor` (default `0.5`)
- `random(min, max)` returns a uniformly distributed value in `[min, max]`

#### Example Delays (with default settings)

| Attempt | Base Delay | Min Delay (factor=0.5) | Max Delay (factor=0.5) |
| ------- | ---------- | ---------------------- | ---------------------- |
| 1       | 2s         | 1.0s                   | 3.0s                   |
| 2       | 4s         | 2.0s                   | 6.0s                   |
| 3       | 8s         | 4.0s                   | 12.0s                  |
| 4       | 16s        | 8.0s                   | 24.0s                  |

### Retry-After Header

When the server includes a `Retry-After` header in the response, the SDK uses the header value directly as the delay in seconds instead of computing an exponential backoff delay. This applies to any retryable response that includes the header, including:

- `202 Accepted` with `Retry-After` (long-running operations)
- `429 Too Many Requests` with `Retry-After`
- `5xx` server errors with `Retry-After`

The header value is parsed as a floating-point number representing seconds.

### Network Exception Handling

Network-level failures (connection refused, DNS resolution errors, timeouts, TLS errors) are represented internally as responses with status `0`. These exceptions are tracked by a **separate counter** (`max_retries_on_exception`, default `2`) from the regular HTTP error retry counter (`max_attempts`).

This means:

- Network exception retries are tracked independently from HTTP error retries, each with their own counter and backoff progression.
- A request can fail up to `max_retries_on_exception` times due to network exceptions, but each exception retry also increments the overall attempt counter, so the total number of retries across both exception and HTTP error types is bounded by `max_attempts`.

### Customizing Retry Parameters

You can customize all retry parameters by initializing `BoxRetryStrategy` with the desired values and passing it to `NetworkSession`:

```python
from box_sdk_gen import (
    BoxClient,
    BoxDeveloperTokenAuth,
    NetworkSession,
    BoxRetryStrategy,
)

auth = BoxDeveloperTokenAuth(token="DEVELOPER_TOKEN_GOES_HERE")
network_session = NetworkSession(
    retry_strategy=BoxRetryStrategy(
        max_attempts=3,
        retry_base_interval=2,
        retry_randomization_factor=0.3,
        max_retries_on_exception=1,
    )
)
client = BoxClient(auth=auth, network_session=network_session)
```

### Custom Retry Strategy

You can implement your own retry strategy by subclassing `RetryStrategy` and overriding the `should_retry` and `retry_after` methods:

```python
from box_sdk_gen import (
    BoxClient,
    BoxDeveloperTokenAuth,
    NetworkSession,
    RetryStrategy,
    FetchOptions,
    FetchResponse,
)


class CustomRetryStrategy(RetryStrategy):
    def should_retry(
        self,
        fetch_options: FetchOptions,
        fetch_response: FetchResponse,
        attempt_number: int,
    ) -> bool:
        return fetch_response.status >= 500 and attempt_number < 3

    def retry_after(
        self,
        fetch_options: FetchOptions,
        fetch_response: FetchResponse,
        attempt_number: int,
    ) -> float:
        return 1.0


auth = BoxDeveloperTokenAuth(token="DEVELOPER_TOKEN_GOES_HERE")
network_session = NetworkSession(retry_strategy=CustomRetryStrategy())
client = BoxClient(auth=auth, network_session=network_session)
```

## Timeouts

You can configure network timeouts with `TimeoutConfig` on `NetworkSession`.
Python SDK supports separate connection and read timeout values in milliseconds.

```python
from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth, NetworkSession, TimeoutConfig

auth = BoxDeveloperTokenAuth(token="DEVELOPER_TOKEN_GOES_HERE")
timeout_config = TimeoutConfig(
    connection_timeout_ms=10000,
    read_timeout_ms=30000,
)
network_session = NetworkSession(timeout_config=timeout_config)
client = BoxClient(auth=auth, network_session=network_session)
```

How timeout handling works:

- Timeout values are configured in milliseconds and converted to seconds internally for HTTP requests.
- If timeout config is not provided, the SDK uses default timeouts: `connection_timeout_ms=5000` (5 seconds) and `read_timeout_ms=60000` (60 seconds).
- To disable all SDK timeouts, pass `TimeoutConfig(connection_timeout_ms=None, read_timeout_ms=None)` explicitly to `NetworkSession`.
- You can also disable only one timeout by setting one value to `None` (for example, `connection_timeout_ms=None` or `read_timeout_ms=None`). If you provide only the other value (for example, `read_timeout_ms=30000`) and leave one unspecified, the unspecified field remains `None` and that timeout stays disabled.
- Timeout failures are treated as network exceptions, and retry behavior is controlled by the configured retry strategy.
- Timeout applies to a single HTTP request attempt to the Box API (not the total time across all retries).
- If retries are exhausted, the SDK raises `BoxSDKError` with the underlying request exception.
