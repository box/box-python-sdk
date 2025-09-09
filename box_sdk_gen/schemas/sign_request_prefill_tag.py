from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import Date


class SignRequestPrefillTag(BaseObject):
    def __init__(
        self,
        *,
        document_tag_id: Optional[str] = None,
        text_value: Optional[str] = None,
        checkbox_value: Optional[bool] = None,
        date_value: Optional[Date] = None,
        **kwargs
    ):
        """
        :param document_tag_id: This references the ID of a specific tag contained in a file of the signature request., defaults to None
        :type document_tag_id: Optional[str], optional
        :param text_value: Text prefill value., defaults to None
        :type text_value: Optional[str], optional
        :param checkbox_value: Checkbox prefill value., defaults to None
        :type checkbox_value: Optional[bool], optional
        :param date_value: Date prefill value., defaults to None
        :type date_value: Optional[Date], optional
        """
        super().__init__(**kwargs)
        self.document_tag_id = document_tag_id
        self.text_value = text_value
        self.checkbox_value = checkbox_value
        self.date_value = date_value
