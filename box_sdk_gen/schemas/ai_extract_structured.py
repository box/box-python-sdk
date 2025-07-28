from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from typing import Dict

from typing import Union

from box_sdk_gen.schemas.ai_item_base import AiItemBase

from box_sdk_gen.schemas.ai_agent_reference import AiAgentReference

from box_sdk_gen.schemas.ai_agent_extract_structured import AiAgentExtractStructured

from box_sdk_gen.box.errors import BoxSDKError


class AiExtractStructuredMetadataTemplateTypeField(str, Enum):
    METADATA_TEMPLATE = 'metadata_template'


class AiExtractStructuredMetadataTemplateField(BaseObject):
    _discriminator = 'type', {'metadata_template'}

    def __init__(
        self,
        *,
        template_key: Optional[str] = None,
        type: Optional[AiExtractStructuredMetadataTemplateTypeField] = None,
        scope: Optional[str] = None,
        **kwargs
    ):
        """
                :param template_key: The name of the metadata template., defaults to None
                :type template_key: Optional[str], optional
                :param type: Value is always `metadata_template`., defaults to None
                :type type: Optional[AiExtractStructuredMetadataTemplateTypeField], optional
                :param scope: The scope of the metadata template that can either be global or
        enterprise.
        * The **global** scope is used for templates that are
        available to any Box enterprise.
        * The **enterprise** scope represents templates created within a specific enterprise,
          containing the ID of that enterprise., defaults to None
                :type scope: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.template_key = template_key
        self.type = type
        self.scope = scope


class AiExtractStructuredFieldsOptionsField(BaseObject):
    def __init__(self, key: str, **kwargs):
        """
        :param key: A unique identifier for the field.
        :type key: str
        """
        super().__init__(**kwargs)
        self.key = key


class AiExtractStructuredFieldsField(BaseObject):
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
        options: Optional[List[AiExtractStructuredFieldsOptionsField]] = None,
        **kwargs
    ):
        """
        :param key: A unique identifier for the field.
        :type key: str
        :param description: A description of the field., defaults to None
        :type description: Optional[str], optional
        :param display_name: The display name of the field., defaults to None
        :type display_name: Optional[str], optional
        :param prompt: The context about the key that may include how to find and format it., defaults to None
        :type prompt: Optional[str], optional
        :param type: The type of the field. It include but is not limited to string, float, date, enum, and multiSelect., defaults to None
        :type type: Optional[str], optional
        :param options: A list of options for this field. This is most often used in combination with the enum and multiSelect field types., defaults to None
        :type options: Optional[List[AiExtractStructuredFieldsOptionsField]], optional
        """
        super().__init__(**kwargs)
        self.key = key
        self.description = description
        self.display_name = display_name
        self.prompt = prompt
        self.type = type
        self.options = options


class AiExtractStructured(BaseObject):
    def __init__(
        self,
        items: List[AiItemBase],
        *,
        metadata_template: Optional[AiExtractStructuredMetadataTemplateField] = None,
        fields: Optional[List[AiExtractStructuredFieldsField]] = None,
        ai_agent: Optional[Union[AiAgentReference, AiAgentExtractStructured]] = None,
        **kwargs
    ):
        """
                :param items: The items to be processed by the LLM. Currently you can use files only.
                :type items: List[AiItemBase]
                :param metadata_template: The metadata template containing the fields to extract.
        For your request to work, you must provide either `metadata_template` or `fields`, but not both., defaults to None
                :type metadata_template: Optional[AiExtractStructuredMetadataTemplateField], optional
                :param fields: The fields to be extracted from the provided items.
        For your request to work, you must provide either `metadata_template` or `fields`, but not both., defaults to None
                :type fields: Optional[List[AiExtractStructuredFieldsField]], optional
        """
        super().__init__(**kwargs)
        self.items = items
        self.metadata_template = metadata_template
        self.fields = fields
        self.ai_agent = ai_agent
