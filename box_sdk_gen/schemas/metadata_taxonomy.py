from typing import Optional

from typing import List

from typing import Dict

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.metadata_taxonomy_level import MetadataTaxonomyLevel

from box_sdk_gen.box.errors import BoxSDKError


class MetadataTaxonomy(BaseObject):
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
        id: str,
        display_name: str,
        namespace: str,
        *,
        key: Optional[str] = None,
        levels: Optional[List[MetadataTaxonomyLevel]] = None,
        **kwargs
    ):
        """
                :param id: A unique identifier of the metadata taxonomy.
                :type id: str
                :param display_name: The display name of the metadata taxonomy. This can be seen in the Box web app.
                :type display_name: str
                :param namespace: A namespace that the metadata taxonomy is associated with.
                :type namespace: str
                :param key: A unique identifier of the metadata taxonomy. The identifier must be unique within
        the namespace to which it belongs., defaults to None
                :type key: Optional[str], optional
                :param levels: Levels of the metadata taxonomy., defaults to None
                :type levels: Optional[List[MetadataTaxonomyLevel]], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.display_name = display_name
        self.namespace = namespace
        self.key = key
        self.levels = levels
