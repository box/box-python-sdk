from enum import Enum

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ClassificationTemplateField(str, Enum):
    SECURITYCLASSIFICATION_6VMVOCHWUWO = 'securityClassification-6VMVochwUWo'


class Classification(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'box_security_classification_key': 'Box__Security__Classification__Key',
        'parent': '$parent',
        'template': '$template',
        'scope': '$scope',
        'version': '$version',
        'type': '$type',
        'type_version': '$typeVersion',
        'can_edit': '$canEdit',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'Box__Security__Classification__Key': 'box_security_classification_key',
        '$parent': 'parent',
        '$template': 'template',
        '$scope': 'scope',
        '$version': 'version',
        '$type': 'type',
        '$typeVersion': 'type_version',
        '$canEdit': 'can_edit',
        **BaseObject._json_to_fields_mapping,
    }

    def __init__(
        self,
        *,
        box_security_classification_key: Optional[str] = None,
        parent: Optional[str] = None,
        template: Optional[ClassificationTemplateField] = None,
        scope: Optional[str] = None,
        version: Optional[int] = None,
        type: Optional[str] = None,
        type_version: Optional[float] = None,
        can_edit: Optional[bool] = None,
        **kwargs
    ):
        """
                :param box_security_classification_key: The name of the classification applied to the item., defaults to None
                :type box_security_classification_key: Optional[str], optional
                :param parent: The identifier of the item that this metadata instance
        has been attached to. This combines the `type` and the `id`
        of the parent in the form `{type}_{id}`., defaults to None
                :type parent: Optional[str], optional
                :param template: The value will always be `securityClassification-6VMVochwUWo`., defaults to None
                :type template: Optional[ClassificationTemplateField], optional
                :param scope: The scope of the enterprise that this classification has been
        applied for.

        This will be in the format `enterprise_{enterprise_id}`., defaults to None
                :type scope: Optional[str], optional
                :param version: The version of the metadata instance. This version starts at 0 and
        increases every time a classification is updated., defaults to None
                :type version: Optional[int], optional
                :param type: The unique ID of this classification instance. This will be include
        the name of the classification template and a unique ID., defaults to None
                :type type: Optional[str], optional
                :param type_version: The version of the metadata template. This version starts at 0 and
        increases every time the template is updated. This is mostly for internal
        use., defaults to None
                :type type_version: Optional[float], optional
                :param can_edit: Whether an end user can change the classification., defaults to None
                :type can_edit: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.box_security_classification_key = box_security_classification_key
        self.parent = parent
        self.template = template
        self.scope = scope
        self.version = version
        self.type = type
        self.type_version = type_version
        self.can_edit = can_edit
