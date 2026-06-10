from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from typing import Dict

from box_sdk_gen.schemas.ai_agent_reference import AiAgentReference

from box_sdk_gen.schemas.ai_agent_extract_structured import AiAgentExtractStructured

from box_sdk_gen.schemas.ai_taxonomy_reference import AiTaxonomyReference

from box_sdk_gen.schemas.ai_taxonomy_file_reference import AiTaxonomyFileReference

from box_sdk_gen.schemas.ai_item_base import AiItemBase

from box_sdk_gen.schemas.ai_extract_sub_field import AiExtractSubField

from box_sdk_gen.schemas.ai_options_rules import AiOptionsRules

from box_sdk_gen.schemas.ai_extract_structured_agent import AiExtractStructuredAgent

from box_sdk_gen.schemas.ai_taxonomy_source import AiTaxonomySource

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
        :param key: A unique identifier for the option.
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
        fields: Optional[List[AiExtractSubField]] = None,
        taxonomy_key: Optional[str] = None,
        namespace: Optional[str] = None,
        options_rules: Optional[AiOptionsRules] = None,
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
        :param type: The type of the field. It can include but is not limited to `string`, `float`, `date`, `enum`, `multiSelect`,`taxonomy`, `struct`, and `table`., defaults to None
        :type type: Optional[str], optional
        :param options: A list of options for this field. This is most often used in combination with the `enum` and `multiSelect` field types., defaults to None
        :type options: Optional[List[AiExtractStructuredFieldsOptionsField]], optional
        :param fields: The nested fields for this field. Used with `struct` and `table` field types to define the nested structure., defaults to None
        :type fields: Optional[List[AiExtractSubField]], optional
        :param taxonomy_key: The identifier for a taxonomy, which corresponds to the `key` of the taxonomy source. Required if using `taxonomy` type field., defaults to None
        :type taxonomy_key: Optional[str], optional
        :param namespace: The namespace of the taxonomy source. Required if using `taxonomy` type field from an existing taxonomy., defaults to None
        :type namespace: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.key = key
        self.description = description
        self.display_name = display_name
        self.prompt = prompt
        self.type = type
        self.options = options
        self.fields = fields
        self.taxonomy_key = taxonomy_key
        self.namespace = namespace
        self.options_rules = options_rules


class AiExtractStructured(BaseObject):
    def __init__(
        self,
        items: List[AiItemBase],
        *,
        metadata_template: Optional[AiExtractStructuredMetadataTemplateField] = None,
        fields: Optional[List[AiExtractStructuredFieldsField]] = None,
        ai_agent: Optional[AiExtractStructuredAgent] = None,
        include_confidence_score: Optional[bool] = None,
        include_reference: Optional[bool] = None,
        taxonomy_sources: Optional[List[AiTaxonomySource]] = None,
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
                :param include_confidence_score: A flag to indicate whether confidence scores for every extracted field should be returned., defaults to None
                :type include_confidence_score: Optional[bool], optional
                :param include_reference: A flag to indicate whether references for every extracted field should be returned., defaults to None
                :type include_reference: Optional[bool], optional
                :param taxonomy_sources: The taxonomy sources to be used for the structured extraction. They can either be an existing file or a taxonomy.
        For your request to work, `fields` must also be provided. `taxonomy_sources` is not supported with `metadata_template`., defaults to None
                :type taxonomy_sources: Optional[List[AiTaxonomySource]], optional
        """
        super().__init__(**kwargs)
        self.items = items
        self.metadata_template = metadata_template
        self.fields = fields
        self.ai_agent = ai_agent
        self.include_confidence_score = include_confidence_score
        self.include_reference = include_reference
        self.taxonomy_sources = taxonomy_sources
