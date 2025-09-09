from enum import Enum

from typing import Optional

from box_sdk_gen.internal.utils import Date

from box_sdk_gen.schemas.sign_request_prefill_tag import SignRequestPrefillTag

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestSignerInputTypeField(str, Enum):
    SIGNATURE = 'signature'
    DATE = 'date'
    TEXT = 'text'
    CHECKBOX = 'checkbox'
    RADIO = 'radio'
    DROPDOWN = 'dropdown'


class SignRequestSignerInputContentTypeField(str, Enum):
    SIGNATURE = 'signature'
    INITIAL = 'initial'
    STAMP = 'stamp'
    DATE = 'date'
    CHECKBOX = 'checkbox'
    TEXT = 'text'
    FULL_NAME = 'full_name'
    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'
    COMPANY = 'company'
    TITLE = 'title'
    EMAIL = 'email'
    ATTACHMENT = 'attachment'
    RADIO = 'radio'
    DROPDOWN = 'dropdown'


class SignRequestSignerInput(SignRequestPrefillTag):
    def __init__(
        self,
        page_index: int,
        *,
        type: Optional[SignRequestSignerInputTypeField] = None,
        content_type: Optional[SignRequestSignerInputContentTypeField] = None,
        read_only: Optional[bool] = None,
        document_tag_id: Optional[str] = None,
        text_value: Optional[str] = None,
        checkbox_value: Optional[bool] = None,
        date_value: Optional[Date] = None,
        **kwargs
    ):
        """
        :param page_index: Index of page that the input is on.
        :type page_index: int
        :param type: Type of input., defaults to None
        :type type: Optional[SignRequestSignerInputTypeField], optional
        :param content_type: Content type of input., defaults to None
        :type content_type: Optional[SignRequestSignerInputContentTypeField], optional
        :param read_only: Whether this input was defined as read-only(immutable by signers) or not., defaults to None
        :type read_only: Optional[bool], optional
        :param document_tag_id: This references the ID of a specific tag contained in a file of the signature request., defaults to None
        :type document_tag_id: Optional[str], optional
        :param text_value: Text prefill value., defaults to None
        :type text_value: Optional[str], optional
        :param checkbox_value: Checkbox prefill value., defaults to None
        :type checkbox_value: Optional[bool], optional
        :param date_value: Date prefill value., defaults to None
        :type date_value: Optional[Date], optional
        """
        super().__init__(
            document_tag_id=document_tag_id,
            text_value=text_value,
            checkbox_value=checkbox_value,
            date_value=date_value,
            **kwargs
        )
        self.page_index = page_index
        self.type = type
        self.content_type = content_type
        self.read_only = read_only
