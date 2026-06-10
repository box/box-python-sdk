from typing import Optional

from typing import List

from typing import Dict

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.ai_extract_field_option import AiExtractFieldOption

from box_sdk_gen.box.errors import BoxSDKError


class AiExtractSubField(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'display_name': 'displayName',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'displayName': 'display_name',
        **BaseObject._json_to_fields_mapping,
    }

    def __init__(
        self,
        key: str,
        *,
        description: Optional[str] = None,
        display_name: Optional[str] = None,
        prompt: Optional[str] = None,
        type: Optional[str] = None,
        options: Optional[List[AiExtractFieldOption]] = None,
        **kwargs
    ):
        """
        :param key: A unique identifier for the nested field.
        :type key: str
        :param description: A description of the nested field., defaults to None
        :type description: Optional[str], optional
        :param display_name: The display name of the nested field., defaults to None
        :type display_name: Optional[str], optional
        :param prompt: Context about the nested field that may include how to find and how to format it., defaults to None
        :type prompt: Optional[str], optional
        :param type: The type of the nested field. Allowed types include `string`, `float`, `date`, `number`, `text`, `boolean`, `enum` and `multiSelect`., defaults to None
        :type type: Optional[str], optional
        :param options: A list of options for this nested field. Used with `enum` and `multiSelect` types., defaults to None
        :type options: Optional[List[AiExtractFieldOption]], optional
        """
        super().__init__(**kwargs)
        self.key = key
        self.description = description
        self.display_name = display_name
        self.prompt = prompt
        self.type = type
        self.options = options
