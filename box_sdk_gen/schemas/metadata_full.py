from typing import Optional

from typing import Dict

from box_sdk_gen.schemas.metadata_base import MetadataBase

from box_sdk_gen.schemas.metadata import Metadata

from box_sdk_gen.box.errors import BoxSDKError


class MetadataFull(Metadata):
    _fields_to_json_mapping: Dict[str, str] = {
        'can_edit': '$canEdit',
        'id': '$id',
        'type': '$type',
        'type_version': '$typeVersion',
        **Metadata._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        '$canEdit': 'can_edit',
        '$id': 'id',
        '$type': 'type',
        '$typeVersion': 'type_version',
        **Metadata._json_to_fields_mapping,
    }

    def __init__(
        self,
        *,
        can_edit: Optional[bool] = None,
        id: Optional[str] = None,
        type: Optional[str] = None,
        type_version: Optional[int] = None,
        parent: Optional[str] = None,
        template: Optional[str] = None,
        scope: Optional[str] = None,
        version: Optional[int] = None,
        **kwargs
    ):
        """
                :param can_edit: Whether the user can edit this metadata instance., defaults to None
                :type can_edit: Optional[bool], optional
                :param id: A UUID to identify the metadata instance., defaults to None
                :type id: Optional[str], optional
                :param type: A unique identifier for the "type" of this instance. This is an
        internal system property and should not be used by a client
        application., defaults to None
                :type type: Optional[str], optional
                :param type_version: The last-known version of the template of the object. This is an
        internal system property and should not be used by a client
        application., defaults to None
                :type type_version: Optional[int], optional
                :param parent: The identifier of the item that this metadata instance
        has been attached to. This combines the `type` and the `id`
        of the parent in the form `{type}_{id}`., defaults to None
                :type parent: Optional[str], optional
                :param template: The name of the template., defaults to None
                :type template: Optional[str], optional
                :param scope: An ID for the scope in which this template
        has been applied. This will be `enterprise_{enterprise_id}` for templates
        defined for use in this enterprise, and `global` for general templates
        that are available to all enterprises using Box., defaults to None
                :type scope: Optional[str], optional
                :param version: The version of the metadata instance. This version starts at 0 and
        increases every time a user-defined property is modified., defaults to None
                :type version: Optional[int], optional
        """
        super().__init__(
            parent=parent, template=template, scope=scope, version=version, **kwargs
        )
        self.can_edit = can_edit
        self.id = id
        self.type = type
        self.type_version = type_version
        self.extra_data = kwargs
