from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from typing import Dict

from box_sdk_gen.schemas.client_error import ClientErrorTypeField

from box_sdk_gen.schemas.client_error import ClientErrorCodeField

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.file_conflict import FileConflict

from box_sdk_gen.box.errors import BoxSDKError


class ConflictErrorContextInfoField(BaseObject):
    def __init__(self, *, conflicts: Optional[List[FileConflict]] = None, **kwargs):
        """
        :param conflicts: A list of the file conflicts that caused this error., defaults to None
        :type conflicts: Optional[List[FileConflict]], optional
        """
        super().__init__(**kwargs)
        self.conflicts = conflicts


class ConflictError(ClientError):
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
        super().__init__(
            type=type,
            status=status,
            code=code,
            message=message,
            context_info=context_info,
            help_url=help_url,
            request_id=request_id,
            **kwargs
        )
