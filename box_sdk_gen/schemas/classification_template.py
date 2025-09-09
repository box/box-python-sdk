from enum import Enum

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.box.errors import BoxSDKError


class ClassificationTemplateTypeField(str, Enum):
    METADATA_TEMPLATE = 'metadata_template'


class ClassificationTemplateTemplateKeyField(str, Enum):
    SECURITYCLASSIFICATION_6VMVOCHWUWO = 'securityClassification-6VMVochwUWo'


class ClassificationTemplateDisplayNameField(str, Enum):
    CLASSIFICATION = 'Classification'


class ClassificationTemplateFieldsTypeField(str, Enum):
    ENUM = 'enum'


class ClassificationTemplateFieldsKeyField(str, Enum):
    BOX__SECURITY__CLASSIFICATION__KEY = 'Box__Security__Classification__Key'


class ClassificationTemplateFieldsDisplayNameField(str, Enum):
    CLASSIFICATION = 'Classification'


class ClassificationTemplateFieldsOptionsStaticConfigClassificationField(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'classification_definition': 'classificationDefinition',
        'color_id': 'colorID',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'classificationDefinition': 'classification_definition',
        'colorID': 'color_id',
        **BaseObject._json_to_fields_mapping,
    }

    def __init__(
        self,
        *,
        classification_definition: Optional[str] = None,
        color_id: Optional[int] = None,
        **kwargs
    ):
        """
                :param classification_definition: A longer description of the classification., defaults to None
                :type classification_definition: Optional[str], optional
                :param color_id: An internal Box identifier used to assign a color to
        a classification label.

        Mapping between a `colorID` and a color may change
        without notice. Currently, the color mappings are as
        follows.

        * `0`: Yellow.
        * `1`: Orange.
        * `2`: Watermelon red.
        * `3`: Purple rain.
        * `4`: Light blue.
        * `5`: Dark blue.
        * `6`: Light green.
        * `7`: Gray., defaults to None
                :type color_id: Optional[int], optional
        """
        super().__init__(**kwargs)
        self.classification_definition = classification_definition
        self.color_id = color_id


class ClassificationTemplateFieldsOptionsStaticConfigField(BaseObject):
    def __init__(
        self,
        *,
        classification: Optional[
            ClassificationTemplateFieldsOptionsStaticConfigClassificationField
        ] = None,
        **kwargs
    ):
        """
                :param classification: Additional information about the classification.

        This is not an exclusive list of properties, and
        more object fields might be returned. These fields
        are used for internal Box Shield and Box Governance
        purposes and no additional value must be derived from
        these fields., defaults to None
                :type classification: Optional[ClassificationTemplateFieldsOptionsStaticConfigClassificationField], optional
        """
        super().__init__(**kwargs)
        self.classification = classification


class ClassificationTemplateFieldsOptionsField(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'static_config': 'staticConfig',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'staticConfig': 'static_config',
        **BaseObject._json_to_fields_mapping,
    }

    def __init__(
        self,
        id: str,
        key: str,
        *,
        static_config: Optional[
            ClassificationTemplateFieldsOptionsStaticConfigField
        ] = None,
        **kwargs
    ):
        """
        :param id: The unique ID of this classification.
        :type id: str
        :param key: The display name and key for this classification.
        :type key: str
        :param static_config: Additional information about the classification., defaults to None
        :type static_config: Optional[ClassificationTemplateFieldsOptionsStaticConfigField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.key = key
        self.static_config = static_config


class ClassificationTemplateFieldsField(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'display_name': 'displayName',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'displayName': 'display_name',
        **BaseObject._json_to_fields_mapping,
    }
    _discriminator = 'type', {'enum'}

    def __init__(
        self,
        id: str,
        options: List[ClassificationTemplateFieldsOptionsField],
        *,
        type: ClassificationTemplateFieldsTypeField = ClassificationTemplateFieldsTypeField.ENUM,
        key: ClassificationTemplateFieldsKeyField = ClassificationTemplateFieldsKeyField.BOX__SECURITY__CLASSIFICATION__KEY,
        display_name: ClassificationTemplateFieldsDisplayNameField = ClassificationTemplateFieldsDisplayNameField.CLASSIFICATION,
        hidden: Optional[bool] = None,
        **kwargs
    ):
        """
                :param id: The unique ID of the field.
                :type id: str
                :param options: A list of classifications available in this enterprise.
                :type options: List[ClassificationTemplateFieldsOptionsField]
                :param type: The array item type., defaults to ClassificationTemplateFieldsTypeField.ENUM
                :type type: ClassificationTemplateFieldsTypeField, optional
                :param key: Defines classifications
        available in the enterprise., defaults to ClassificationTemplateFieldsKeyField.BOX__SECURITY__CLASSIFICATION__KEY
                :type key: ClassificationTemplateFieldsKeyField, optional
                :param display_name: The value will always be `Classification`., defaults to ClassificationTemplateFieldsDisplayNameField.CLASSIFICATION
                :type display_name: ClassificationTemplateFieldsDisplayNameField, optional
                :param hidden: Classifications are always visible to web and mobile users., defaults to None
                :type hidden: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.options = options
        self.type = type
        self.key = key
        self.display_name = display_name
        self.hidden = hidden


class ClassificationTemplate(BaseObject):
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
        scope: str,
        fields: List[ClassificationTemplateFieldsField],
        *,
        type: ClassificationTemplateTypeField = ClassificationTemplateTypeField.METADATA_TEMPLATE,
        template_key: ClassificationTemplateTemplateKeyField = ClassificationTemplateTemplateKeyField.SECURITYCLASSIFICATION_6VMVOCHWUWO,
        display_name: ClassificationTemplateDisplayNameField = ClassificationTemplateDisplayNameField.CLASSIFICATION,
        hidden: Optional[bool] = None,
        copy_instance_on_item_copy: Optional[bool] = None,
        **kwargs
    ):
        """
                :param id: The ID of the classification template.
                :type id: str
                :param scope: The scope of the classification template. This is in the format
        `enterprise_{id}` where the `id` is the enterprise ID.
                :type scope: str
                :param fields: A list of fields for this classification template. This includes
        only one field, the `Box__Security__Classification__Key`, which defines
        the different classifications available in this enterprise.
                :type fields: List[ClassificationTemplateFieldsField]
                :param type: The value will always be `metadata_template`., defaults to ClassificationTemplateTypeField.METADATA_TEMPLATE
                :type type: ClassificationTemplateTypeField, optional
                :param template_key: The value will always be `securityClassification-6VMVochwUWo`., defaults to ClassificationTemplateTemplateKeyField.SECURITYCLASSIFICATION_6VMVOCHWUWO
                :type template_key: ClassificationTemplateTemplateKeyField, optional
                :param display_name: The name of this template as shown in web and mobile interfaces., defaults to ClassificationTemplateDisplayNameField.CLASSIFICATION
                :type display_name: ClassificationTemplateDisplayNameField, optional
                :param hidden: Determines if the
        template is always available in web and mobile interfaces., defaults to None
                :type hidden: Optional[bool], optional
                :param copy_instance_on_item_copy: Determines if
        classifications are
        copied along when the file or folder is
        copied., defaults to None
                :type copy_instance_on_item_copy: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.scope = scope
        self.fields = fields
        self.type = type
        self.template_key = template_key
        self.display_name = display_name
        self.hidden = hidden
        self.copy_instance_on_item_copy = copy_instance_on_item_copy
