from enum import Enum

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ClientErrorTypeField(str, Enum):
    ERROR = 'error'


class ClientErrorCodeField(str, Enum):
    CREATED = 'created'
    ACCEPTED = 'accepted'
    NO_CONTENT = 'no_content'
    REDIRECT = 'redirect'
    NOT_MODIFIED = 'not_modified'
    BAD_REQUEST = 'bad_request'
    UNAUTHORIZED = 'unauthorized'
    FORBIDDEN = 'forbidden'
    NOT_FOUND = 'not_found'
    METHOD_NOT_ALLOWED = 'method_not_allowed'
    CONFLICT = 'conflict'
    PRECONDITION_FAILED = 'precondition_failed'
    TOO_MANY_REQUESTS = 'too_many_requests'
    INTERNAL_SERVER_ERROR = 'internal_server_error'
    UNAVAILABLE = 'unavailable'
    ITEM_NAME_INVALID = 'item_name_invalid'
    INSUFFICIENT_SCOPE = 'insufficient_scope'


class ClientError(BaseObject):
    _discriminator = 'type', {'error'}

    def __init__(
        self,
        *,
        type: Optional[ClientErrorTypeField] = None,
        status: Optional[int] = None,
        code: Optional[ClientErrorCodeField] = None,
        message: Optional[str] = None,
        context_info: Optional[Dict] = None,
        help_url: Optional[str] = None,
        request_id: Optional[str] = None,
        **kwargs
    ):
        """
                :param type: The value will always be `error`., defaults to None
                :type type: Optional[ClientErrorTypeField], optional
                :param status: The HTTP status of the response., defaults to None
                :type status: Optional[int], optional
                :param code: A Box-specific error code., defaults to None
                :type code: Optional[ClientErrorCodeField], optional
                :param message: A short message describing the error., defaults to None
                :type message: Optional[str], optional
                :param context_info: A free-form object that contains additional context
        about the error. The possible fields are defined on
        a per-endpoint basis. `message` is only one example., defaults to None
                :type context_info: Optional[Dict], optional
                :param help_url: A URL that links to more information about why this error occurred., defaults to None
                :type help_url: Optional[str], optional
                :param request_id: A unique identifier for this response, which can be used
        when contacting Box support., defaults to None
                :type request_id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.status = status
        self.code = code
        self.message = message
        self.context_info = context_info
        self.help_url = help_url
        self.request_id = request_id
