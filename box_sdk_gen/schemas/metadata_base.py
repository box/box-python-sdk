from typing import Optional

from typing import Dict

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class MetadataBase(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'parent': '$parent',
        'template': '$template',
        'scope': '$scope',
        'version': '$version',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        '$parent': 'parent',
        '$template': 'template',
        '$scope': 'scope',
        '$version': 'version',
        **BaseObject._json_to_fields_mapping,
    }

    def __init__(
        self,
        *,
        parent: Optional[str] = None,
        template: Optional[str] = None,
        scope: Optional[str] = None,
        version: Optional[int] = None,
        **kwargs
    ):
        """
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
        super().__init__(**kwargs)
        self.parent = parent
        self.template = template
        self.scope = scope
        self.version = version
