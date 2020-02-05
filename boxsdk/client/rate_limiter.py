import collections
import time


class RateLimiter(object):
    def __init__(
        self,
        rate_limit=1,
        rate_period=12
    ):
        self._rate_limit = rate_limit
        self._rate_period = rate_period
        self._request_pool = collections.deque()

    def _limiter(self):
        while True:
            now = time.time()

            while self._request_pool:
                if now - self._request_pool[0] > self._rate_period:
                    self._request_pool.popleft()
                else:
                    break

            if len(self._request_pool) < self._rate_limit:
                break

            time.sleep(0.01)

        self._request_pool.append(time.time())

    def limit(self):
        self._limiter()

    def __enter__(self):
        return self._limiter()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass
