from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from typing import Dict

from box_sdk_gen.box.errors import BoxSDKError


class MetadataTemplateTypeField(str, Enum):
    METADATA_TEMPLATE = 'metadata_template'


class MetadataTemplateFieldsTypeField(str, Enum):
    STRING = 'string'
    FLOAT = 'float'
    DATE = 'date'
    ENUM = 'enum'
    MULTISELECT = 'multiSelect'
    INTEGER = 'integer'


class MetadataTemplateFieldsOptionsField(BaseObject):
    def __init__(self, key: str, *, id: Optional[str] = None, **kwargs):
        """
                :param key: The text value of the option. This represents both the display name of the
        option and the internal key used when updating templates.
                :type key: str
                :param id: The internal unique identifier of the option., defaults to None
                :type id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.key = key
        self.id = id


class MetadataTemplateFieldsField(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'display_name': 'displayName',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'displayName': 'display_name',
        **BaseObject._json_to_fields_mapping,
    }
    _discriminator = 'type', {
        'string',
        'float',
        'date',
        'enum',
        'multiSelect',
        'integer',
    }

    def __init__(
        self,
        type: MetadataTemplateFieldsTypeField,
        key: str,
        display_name: str,
        *,
        description: Optional[str] = None,
        hidden: Optional[bool] = None,
        options: Optional[List[MetadataTemplateFieldsOptionsField]] = None,
        id: Optional[str] = None,
        **kwargs
    ):
        """
                :param type: The type of field. The basic fields are a `string` field for text, a
        `float` field for numbers, and a `date` fields to present the user with a
        date-time picker.

        Additionally, metadata templates support an `enum` field for a basic list
        of items, and ` multiSelect` field for a similar list of items where the
        user can select more than one value.

        **Note**: The `integer` value is deprecated.
        It is still present in the response,
        but cannot be used in the POST request.
                :type type: MetadataTemplateFieldsTypeField
                :param key: A unique identifier for the field. The identifier must
        be unique within the template to which it belongs.
                :type key: str
                :param display_name: The display name of the field as it is shown to the user in the web and
        mobile apps.
                :type display_name: str
                :param description: A description of the field. This is not shown to the user., defaults to None
                :type description: Optional[str], optional
                :param hidden: Whether this field is hidden in the UI for the user and can only be set
        through the API instead., defaults to None
                :type hidden: Optional[bool], optional
                :param options: A list of options for this field. This is used in combination
        with the `enum` and `multiSelect` field types., defaults to None
                :type options: Optional[List[MetadataTemplateFieldsOptionsField]], optional
                :param id: The unique ID of the metadata template field., defaults to None
                :type id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.key = key
        self.display_name = display_name
        self.description = description
        self.hidden = hidden
        self.options = options
        self.id = id


class MetadataTemplate(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'template_key': 'templateKey',
        'display_name': 'displayName',
        'copy_instance_on_item_copy': 'copyInstanceOnItemCopy',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'templateKey': 'template_key',
        'displayName': 'display_name',
        'copyInstanceOnItemCopy': 'copy_instance_on_item_copy',
        **BaseObject._json_to_fields_mapping,
    }
    _discriminator = 'type', {'metadata_template'}

    def __init__(
        self,
        id: str,
        *,
        type: MetadataTemplateTypeField = MetadataTemplateTypeField.METADATA_TEMPLATE,
        scope: Optional[str] = None,
        template_key: Optional[str] = None,
        display_name: Optional[str] = None,
        hidden: Optional[bool] = None,
        fields: Optional[List[MetadataTemplateFieldsField]] = None,
        copy_instance_on_item_copy: Optional[bool] = None,
        **kwargs
    ):
        """
                :param id: The ID of the metadata template.
                :type id: str
                :param type: The value will always be `metadata_template`., defaults to MetadataTemplateTypeField.METADATA_TEMPLATE
                :type type: MetadataTemplateTypeField, optional
                :param scope: The scope of the metadata template can either be `global` or
        `enterprise_*`. The `global` scope is used for templates that are
        available to any Box enterprise. The `enterprise_*` scope represents
        templates that have been created within a specific enterprise, where `*`
        will be the ID of that enterprise., defaults to None
                :type scope: Optional[str], optional
                :param template_key: A unique identifier for the template. This identifier is unique across
        the `scope` of the enterprise to which the metadata template is being
        applied, yet is not necessarily unique across different enterprises., defaults to None
                :type template_key: Optional[str], optional
                :param display_name: The display name of the template. This can be seen in the Box web app
        and mobile apps., defaults to None
                :type display_name: Optional[str], optional
                :param hidden: Defines if this template is visible in the Box web app UI, or if
        it is purely intended for usage through the API., defaults to None
                :type hidden: Optional[bool], optional
                :param fields: An ordered list of template fields which are part of the template. Each
        field can be a regular text field, date field, number field, as well as a
        single or multi-select list., defaults to None
                :type fields: Optional[List[MetadataTemplateFieldsField]], optional
                :param copy_instance_on_item_copy: Whether or not to include the metadata when a file or folder is copied., defaults to None
                :type copy_instance_on_item_copy: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.scope = scope
        self.template_key = template_key
        self.display_name = display_name
        self.hidden = hidden
        self.fields = fields
        self.copy_instance_on_item_copy = copy_instance_on_item_copy
