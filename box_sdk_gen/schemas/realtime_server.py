from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class RealtimeServer(BaseObject):
    def __init__(
        self,
        *,
        type: Optional[str] = None,
        url: Optional[str] = None,
        ttl: Optional[str] = None,
        max_retries: Optional[str] = None,
        retry_timeout: Optional[int] = None,
        **kwargs
    ):
        """
                :param type: The value will always be `realtime_server`., defaults to None
                :type type: Optional[str], optional
                :param url: The URL for the server., defaults to None
                :type url: Optional[str], optional
                :param ttl: The time in minutes for which this server is available., defaults to None
                :type ttl: Optional[str], optional
                :param max_retries: The maximum number of retries this server will
        allow before a new long poll should be started by
        getting a [new list of server](#options-events)., defaults to None
                :type max_retries: Optional[str], optional
                :param retry_timeout: The maximum number of seconds without a response
        after which you should retry the long poll connection.

        This helps to overcome network issues where the long
        poll looks to be working but no packages are coming
        through., defaults to None
                :type retry_timeout: Optional[int], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.url = url
        self.ttl = ttl
        self.max_retries = max_retries
        self.retry_timeout = retry_timeout
