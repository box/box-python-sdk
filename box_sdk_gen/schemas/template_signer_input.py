from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.internal.utils import Date

from box_sdk_gen.schemas.sign_request_prefill_tag import SignRequestPrefillTag

from box_sdk_gen.box.errors import BoxSDKError


class TemplateSignerInputTypeField(str, Enum):
    SIGNATURE = 'signature'
    DATE = 'date'
    TEXT = 'text'
    CHECKBOX = 'checkbox'
    ATTACHMENT = 'attachment'
    RADIO = 'radio'
    DROPDOWN = 'dropdown'


class TemplateSignerInputContentTypeField(str, Enum):
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


class TemplateSignerInputCoordinatesField(BaseObject):
    def __init__(
        self, *, x: Optional[float] = None, y: Optional[float] = None, **kwargs
    ):
        """
        :param x: Relative x coordinate to the page the input is on, ranging from 0 to 1., defaults to None
        :type x: Optional[float], optional
        :param y: Relative y coordinate to the page the input is on, ranging from 0 to 1., defaults to None
        :type y: Optional[float], optional
        """
        super().__init__(**kwargs)
        self.x = x
        self.y = y


class TemplateSignerInputDimensionsField(BaseObject):
    def __init__(
        self, *, width: Optional[float] = None, height: Optional[float] = None, **kwargs
    ):
        """
        :param width: Relative width to the page the input is on, ranging from 0 to 1., defaults to None
        :type width: Optional[float], optional
        :param height: Relative height to the page the input is on, ranging from 0 to 1., defaults to None
        :type height: Optional[float], optional
        """
        super().__init__(**kwargs)
        self.width = width
        self.height = height


class TemplateSignerInput(SignRequestPrefillTag):
    def __init__(
        self,
        page_index: int,
        *,
        type: Optional[TemplateSignerInputTypeField] = None,
        content_type: Optional[TemplateSignerInputContentTypeField] = None,
        is_required: Optional[bool] = None,
        document_id: Optional[str] = None,
        dropdown_choices: Optional[List[str]] = None,
        group_id: Optional[str] = None,
        coordinates: Optional[TemplateSignerInputCoordinatesField] = None,
        dimensions: Optional[TemplateSignerInputDimensionsField] = None,
        label: Optional[str] = None,
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
                :type type: Optional[TemplateSignerInputTypeField], optional
                :param content_type: Content type of input., defaults to None
                :type content_type: Optional[TemplateSignerInputContentTypeField], optional
                :param is_required: Whether or not the input is required., defaults to None
                :type is_required: Optional[bool], optional
                :param document_id: Document identifier., defaults to None
                :type document_id: Optional[str], optional
                :param dropdown_choices: When the input is of the type `dropdown` this
        values will be filled with all the
        dropdown options., defaults to None
                :type dropdown_choices: Optional[List[str]], optional
                :param group_id: When the input is of type `radio` they can be
        grouped to gather with this identifier., defaults to None
                :type group_id: Optional[str], optional
                :param coordinates: Where the input is located on a page., defaults to None
                :type coordinates: Optional[TemplateSignerInputCoordinatesField], optional
                :param dimensions: The size of the input., defaults to None
                :type dimensions: Optional[TemplateSignerInputDimensionsField], optional
                :param label: The label field is used especially for text, attachment, radio, and checkbox type inputs., defaults to None
                :type label: Optional[str], optional
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
        self.is_required = is_required
        self.document_id = document_id
        self.dropdown_choices = dropdown_choices
        self.group_id = group_id
        self.coordinates = coordinates
        self.dimensions = dimensions
        self.label = label
        self.read_only = read_only
