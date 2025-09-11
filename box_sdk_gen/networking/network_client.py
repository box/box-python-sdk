from abc import abstractmethod

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse


class NetworkClient:
    def __init__(self):
        pass

    @abstractmethod
    def fetch(self, options: FetchOptions) -> FetchResponse:
        pass
