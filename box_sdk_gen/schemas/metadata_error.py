from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class MetadataError(BaseObject):
    def __init__(
        self,
        *,
        code: Optional[str] = None,
        message: Optional[str] = None,
        request_id: Optional[str] = None,
        **kwargs
    ):
        """
                :param code: A Box-specific error code., defaults to None
                :type code: Optional[str], optional
                :param message: A short message describing the error., defaults to None
                :type message: Optional[str], optional
                :param request_id: A unique identifier for this response, which can be used
        when contacting Box support., defaults to None
                :type request_id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.code = code
        self.message = message
        self.request_id = request_id
