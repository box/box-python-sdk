from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import Dict

from box_sdk_gen.box.errors import BoxSDKError


class MetadataCascadePolicyTypeField(str, Enum):
    METADATA_CASCADE_POLICY = 'metadata_cascade_policy'


class MetadataCascadePolicyOwnerEnterpriseTypeField(str, Enum):
    ENTERPRISE = 'enterprise'


class MetadataCascadePolicyOwnerEnterpriseField(BaseObject):
    _discriminator = 'type', {'enterprise'}

    def __init__(
        self,
        *,
        type: Optional[MetadataCascadePolicyOwnerEnterpriseTypeField] = None,
        id: Optional[str] = None,
        **kwargs
    ):
        """
        :param type: The value will always be `enterprise`., defaults to None
        :type type: Optional[MetadataCascadePolicyOwnerEnterpriseTypeField], optional
        :param id: The ID of the enterprise that owns the policy., defaults to None
        :type id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id


class MetadataCascadePolicyParentTypeField(str, Enum):
    FOLDER = 'folder'


class MetadataCascadePolicyParentField(BaseObject):
    _discriminator = 'type', {'folder'}

    def __init__(
        self,
        *,
        type: Optional[MetadataCascadePolicyParentTypeField] = None,
        id: Optional[str] = None,
        **kwargs
    ):
        """
        :param type: The value will always be `folder`., defaults to None
        :type type: Optional[MetadataCascadePolicyParentTypeField], optional
        :param id: The ID of the folder the policy is applied to., defaults to None
        :type id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id


class MetadataCascadePolicy(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'template_key': 'templateKey',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'templateKey': 'template_key',
        **BaseObject._json_to_fields_mapping,
    }
    _discriminator = 'type', {'metadata_cascade_policy'}

    def __init__(
        self,
        id: str,
        *,
        type: MetadataCascadePolicyTypeField = MetadataCascadePolicyTypeField.METADATA_CASCADE_POLICY,
        owner_enterprise: Optional[MetadataCascadePolicyOwnerEnterpriseField] = None,
        parent: Optional[MetadataCascadePolicyParentField] = None,
        scope: Optional[str] = None,
        template_key: Optional[str] = None,
        **kwargs
    ):
        """
                :param id: The ID of the metadata cascade policy object.
                :type id: str
                :param type: The value will always be `metadata_cascade_policy`., defaults to MetadataCascadePolicyTypeField.METADATA_CASCADE_POLICY
                :type type: MetadataCascadePolicyTypeField, optional
                :param owner_enterprise: The enterprise that owns this policy., defaults to None
                :type owner_enterprise: Optional[MetadataCascadePolicyOwnerEnterpriseField], optional
                :param parent: Represent the folder the policy is applied to., defaults to None
                :type parent: Optional[MetadataCascadePolicyParentField], optional
                :param scope: The scope of the metadata cascade policy can either be `global` or
        `enterprise_*`. The `global` scope is used for policies that are
        available to any Box enterprise. The `enterprise_*` scope represents
        policies that have been created within a specific enterprise, where `*`
        will be the ID of that enterprise., defaults to None
                :type scope: Optional[str], optional
                :param template_key: The key of the template that is cascaded down to the folder's
        children.

        In many cases the template key is automatically derived
        of its display name, for example `Contract Template` would
        become `contractTemplate`. In some cases the creator of the
        template will have provided its own template key.

        Please [list the templates for an enterprise][list], or
        get all instances on a [file][file] or [folder][folder]
        to inspect a template's key.

        [list]: e://get-metadata-templates-enterprise
        [file]: e://get-files-id-metadata
        [folder]: e://get-folders-id-metadata, defaults to None
                :type template_key: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.owner_enterprise = owner_enterprise
        self.parent = parent
        self.scope = scope
        self.template_key = template_key
