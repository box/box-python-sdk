from .developer_token_client import DeveloperTokenClient
from .logging_client import LoggingClient


class DevelopmentClient(LoggingClient, DeveloperTokenClient):
    """
    Client subclass that uses developer token auth and logs requests and responses.
    Great for use in development!
    """
