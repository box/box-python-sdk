from enum import Enum

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.classification_template import ClassificationTemplate

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import prepare_params

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.serialization.json import SerializedData


class AddClassificationRequestBodyOpField(str, Enum):
    ADDENUMOPTION = 'addEnumOption'


class AddClassificationRequestBodyFieldKeyField(str, Enum):
    BOX__SECURITY__CLASSIFICATION__KEY = 'Box__Security__Classification__Key'


class AddClassificationRequestBodyDataStaticConfigClassificationField(BaseObject):
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


class AddClassificationRequestBodyDataStaticConfigField(BaseObject):
    def __init__(
        self,
        *,
        classification: Optional[
            AddClassificationRequestBodyDataStaticConfigClassificationField
        ] = None,
        **kwargs
    ):
        """
        :param classification: Additional details for the classification., defaults to None
        :type classification: Optional[AddClassificationRequestBodyDataStaticConfigClassificationField], optional
        """
        super().__init__(**kwargs)
        self.classification = classification


class AddClassificationRequestBodyDataField(BaseObject):
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
        key: str,
        *,
        static_config: Optional[
            AddClassificationRequestBodyDataStaticConfigField
        ] = None,
        **kwargs
    ):
        """
                :param key: The label of the classification as shown in the web and
        mobile interfaces. This is the only field required to
        add a classification.
                :type key: str
                :param static_config: A static configuration for the classification., defaults to None
                :type static_config: Optional[AddClassificationRequestBodyDataStaticConfigField], optional
        """
        super().__init__(**kwargs)
        self.key = key
        self.static_config = static_config


class AddClassificationRequestBody(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'field_key': 'fieldKey',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'fieldKey': 'field_key',
        **BaseObject._json_to_fields_mapping,
    }

    def __init__(
        self,
        data: AddClassificationRequestBodyDataField,
        *,
        op: AddClassificationRequestBodyOpField = AddClassificationRequestBodyOpField.ADDENUMOPTION,
        field_key: AddClassificationRequestBodyFieldKeyField = AddClassificationRequestBodyFieldKeyField.BOX__SECURITY__CLASSIFICATION__KEY,
        **kwargs
    ):
        """
                :param data: The details of the classification to add.
                :type data: AddClassificationRequestBodyDataField
                :param op: The type of change to perform on the classification
        object., defaults to AddClassificationRequestBodyOpField.ADDENUMOPTION
                :type op: AddClassificationRequestBodyOpField, optional
                :param field_key: Defines classifications
        available in the enterprise., defaults to AddClassificationRequestBodyFieldKeyField.BOX__SECURITY__CLASSIFICATION__KEY
                :type field_key: AddClassificationRequestBodyFieldKeyField, optional
        """
        super().__init__(**kwargs)
        self.data = data
        self.op = op
        self.field_key = field_key


class UpdateClassificationRequestBodyOpField(str, Enum):
    EDITENUMOPTION = 'editEnumOption'


class UpdateClassificationRequestBodyFieldKeyField(str, Enum):
    BOX__SECURITY__CLASSIFICATION__KEY = 'Box__Security__Classification__Key'


class UpdateClassificationRequestBodyDataStaticConfigClassificationField(BaseObject):
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


class UpdateClassificationRequestBodyDataStaticConfigField(BaseObject):
    def __init__(
        self,
        *,
        classification: Optional[
            UpdateClassificationRequestBodyDataStaticConfigClassificationField
        ] = None,
        **kwargs
    ):
        """
        :param classification: Additional details for the classification., defaults to None
        :type classification: Optional[UpdateClassificationRequestBodyDataStaticConfigClassificationField], optional
        """
        super().__init__(**kwargs)
        self.classification = classification


class UpdateClassificationRequestBodyDataField(BaseObject):
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
        key: str,
        *,
        static_config: Optional[
            UpdateClassificationRequestBodyDataStaticConfigField
        ] = None,
        **kwargs
    ):
        """
                :param key: A new label for the classification, as it will be
        shown in the web and mobile interfaces.
                :type key: str
                :param static_config: A static configuration for the classification., defaults to None
                :type static_config: Optional[UpdateClassificationRequestBodyDataStaticConfigField], optional
        """
        super().__init__(**kwargs)
        self.key = key
        self.static_config = static_config


class UpdateClassificationRequestBody(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'field_key': 'fieldKey',
        'enum_option_key': 'enumOptionKey',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'fieldKey': 'field_key',
        'enumOptionKey': 'enum_option_key',
        **BaseObject._json_to_fields_mapping,
    }

    def __init__(
        self,
        enum_option_key: str,
        data: UpdateClassificationRequestBodyDataField,
        *,
        op: UpdateClassificationRequestBodyOpField = UpdateClassificationRequestBodyOpField.EDITENUMOPTION,
        field_key: UpdateClassificationRequestBodyFieldKeyField = UpdateClassificationRequestBodyFieldKeyField.BOX__SECURITY__CLASSIFICATION__KEY,
        **kwargs
    ):
        """
                :param enum_option_key: The original label of the classification to change.
                :type enum_option_key: str
                :param data: The details of the updated classification.
                :type data: UpdateClassificationRequestBodyDataField
                :param op: The type of change to perform on the classification
        object., defaults to UpdateClassificationRequestBodyOpField.EDITENUMOPTION
                :type op: UpdateClassificationRequestBodyOpField, optional
                :param field_key: Defines classifications
        available in the enterprise., defaults to UpdateClassificationRequestBodyFieldKeyField.BOX__SECURITY__CLASSIFICATION__KEY
                :type field_key: UpdateClassificationRequestBodyFieldKeyField, optional
        """
        super().__init__(**kwargs)
        self.enum_option_key = enum_option_key
        self.data = data
        self.op = op
        self.field_key = field_key


class CreateClassificationTemplateScope(str, Enum):
    ENTERPRISE = 'enterprise'


class CreateClassificationTemplateTemplateKey(str, Enum):
    SECURITYCLASSIFICATION_6VMVOCHWUWO = 'securityClassification-6VMVochwUWo'


class CreateClassificationTemplateDisplayName(str, Enum):
    CLASSIFICATION = 'Classification'


class CreateClassificationTemplateFieldsTypeField(str, Enum):
    ENUM = 'enum'


class CreateClassificationTemplateFieldsKeyField(str, Enum):
    BOX__SECURITY__CLASSIFICATION__KEY = 'Box__Security__Classification__Key'


class CreateClassificationTemplateFieldsDisplayNameField(str, Enum):
    CLASSIFICATION = 'Classification'


class CreateClassificationTemplateFieldsOptionsStaticConfigClassificationField(
    BaseObject
):
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
                :param color_id: An identifier used to assign a color to
        a classification label.

        Mapping between a `colorID` and a color may
        change without notice. Currently, the color
        mappings are as follows.

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


class CreateClassificationTemplateFieldsOptionsStaticConfigField(BaseObject):
    def __init__(
        self,
        *,
        classification: Optional[
            CreateClassificationTemplateFieldsOptionsStaticConfigClassificationField
        ] = None,
        **kwargs
    ):
        """
        :param classification: Additional information about the classification., defaults to None
        :type classification: Optional[CreateClassificationTemplateFieldsOptionsStaticConfigClassificationField], optional
        """
        super().__init__(**kwargs)
        self.classification = classification


class CreateClassificationTemplateFieldsOptionsField(BaseObject):
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
        key: str,
        *,
        static_config: Optional[
            CreateClassificationTemplateFieldsOptionsStaticConfigField
        ] = None,
        **kwargs
    ):
        """
                :param key: The display name and key this classification. This
        will be show in the Box UI.
                :type key: str
                :param static_config: Additional information about the classification., defaults to None
                :type static_config: Optional[CreateClassificationTemplateFieldsOptionsStaticConfigField], optional
        """
        super().__init__(**kwargs)
        self.key = key
        self.static_config = static_config


class CreateClassificationTemplateFields(BaseObject):
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
        options: List[CreateClassificationTemplateFieldsOptionsField],
        *,
        type: CreateClassificationTemplateFieldsTypeField = CreateClassificationTemplateFieldsTypeField.ENUM,
        key: CreateClassificationTemplateFieldsKeyField = CreateClassificationTemplateFieldsKeyField.BOX__SECURITY__CLASSIFICATION__KEY,
        display_name: CreateClassificationTemplateFieldsDisplayNameField = CreateClassificationTemplateFieldsDisplayNameField.CLASSIFICATION,
        hidden: Optional[bool] = None,
        **kwargs
    ):
        """
                :param options: The actual list of classifications that are present on
        this template.
                :type options: List[CreateClassificationTemplateFieldsOptionsField]
                :param type: The type of the field
        that is always enum., defaults to CreateClassificationTemplateFieldsTypeField.ENUM
                :type type: CreateClassificationTemplateFieldsTypeField, optional
                :param key: Defines classifications
        available in the enterprise., defaults to CreateClassificationTemplateFieldsKeyField.BOX__SECURITY__CLASSIFICATION__KEY
                :type key: CreateClassificationTemplateFieldsKeyField, optional
                :param display_name: A display name for the classification., defaults to CreateClassificationTemplateFieldsDisplayNameField.CLASSIFICATION
                :type display_name: CreateClassificationTemplateFieldsDisplayNameField, optional
                :param hidden: Determines if the classification
        template is
        hidden or available on
        web and mobile
        devices., defaults to None
                :type hidden: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.options = options
        self.type = type
        self.key = key
        self.display_name = display_name
        self.hidden = hidden


class ClassificationsManager:
    def __init__(
        self,
        *,
        auth: Optional[Authentication] = None,
        network_session: NetworkSession = None
    ):
        if network_session is None:
            network_session = NetworkSession()
        self.auth = auth
        self.network_session = network_session

    def get_classification_template(
        self, *, extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ClassificationTemplate:
        """
        Retrieves the classification metadata template and lists all the

        classifications available to this enterprise.


        This API can also be called by including the enterprise ID in the


        URL explicitly, for example


        `/metadata_templates/enterprise_12345/securityClassification-6VMVochwUWo/schema`.

        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/metadata_templates/enterprise/securityClassification-6VMVochwUWo/schema',
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ClassificationTemplate)

    def add_classification(
        self,
        request_body: List[AddClassificationRequestBody],
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ClassificationTemplate:
        """
        Adds one or more new classifications to the list of classifications

        available to the enterprise.


        This API can also be called by including the enterprise ID in the


        URL explicitly, for example


        `/metadata_templates/enterprise_12345/securityClassification-6VMVochwUWo/schema`.

        :param request_body: Request body of addClassification method
        :type request_body: List[AddClassificationRequestBody]
        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/metadata_templates/enterprise/securityClassification-6VMVochwUWo/schema#add',
                    ]
                ),
                method='PUT',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ClassificationTemplate)

    def update_classification(
        self,
        request_body: List[UpdateClassificationRequestBody],
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ClassificationTemplate:
        """
        Updates the labels and descriptions of one or more classifications

        available to the enterprise.


        This API can also be called by including the enterprise ID in the


        URL explicitly, for example


        `/metadata_templates/enterprise_12345/securityClassification-6VMVochwUWo/schema`.

        :param request_body: Request body of updateClassification method
        :type request_body: List[UpdateClassificationRequestBody]
        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/metadata_templates/enterprise/securityClassification-6VMVochwUWo/schema#update',
                    ]
                ),
                method='PUT',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json-patch+json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ClassificationTemplate)

    def create_classification_template(
        self,
        fields: List[CreateClassificationTemplateFields],
        *,
        scope: CreateClassificationTemplateScope = CreateClassificationTemplateScope.ENTERPRISE,
        template_key: CreateClassificationTemplateTemplateKey = CreateClassificationTemplateTemplateKey.SECURITYCLASSIFICATION_6VMVOCHWUWO,
        display_name: CreateClassificationTemplateDisplayName = CreateClassificationTemplateDisplayName.CLASSIFICATION,
        hidden: Optional[bool] = None,
        copy_instance_on_item_copy: Optional[bool] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> ClassificationTemplate:
        """
                When an enterprise does not yet have any classifications, this API call

                initializes the classification template with an initial set of


                classifications.


                If an enterprise already has a classification, the template will already


                exist and instead an API call should be made to add additional


                classifications.

                :param fields: The classification template requires exactly
        one field, which holds
        all the valid classification values.
                :type fields: List[CreateClassificationTemplateFields]
                :param scope: The scope in which to create the classifications. This should
        be `enterprise` or `enterprise_{id}` where `id` is the unique
        ID of the enterprise., defaults to CreateClassificationTemplateScope.ENTERPRISE
                :type scope: CreateClassificationTemplateScope, optional
                :param template_key: Defines the list of metadata templates., defaults to CreateClassificationTemplateTemplateKey.SECURITYCLASSIFICATION_6VMVOCHWUWO
                :type template_key: CreateClassificationTemplateTemplateKey, optional
                :param display_name: The name of the
        template as shown in web and mobile interfaces., defaults to CreateClassificationTemplateDisplayName.CLASSIFICATION
                :type display_name: CreateClassificationTemplateDisplayName, optional
                :param hidden: Determines if the classification template is
        hidden or available on web and mobile
        devices., defaults to None
                :type hidden: Optional[bool], optional
                :param copy_instance_on_item_copy: Determines if classifications are
        copied along when the file or folder is
        copied., defaults to None
                :type copy_instance_on_item_copy: Optional[bool], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'scope': scope,
            'templateKey': template_key,
            'displayName': display_name,
            'hidden': hidden,
            'copyInstanceOnItemCopy': copy_instance_on_item_copy,
            'fields': fields,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/metadata_templates/schema#classifications',
                    ]
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, ClassificationTemplate)
