from typing import Optional

from typing import List

from typing import Dict

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.metadata_taxonomy_ancestor import MetadataTaxonomyAncestor

from box_sdk_gen.box.errors import BoxSDKError


class MetadataTaxonomyNode(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'display_name': 'displayName',
        'parent_id': 'parentId',
        'node_path': 'nodePath',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'displayName': 'display_name',
        'parentId': 'parent_id',
        'nodePath': 'node_path',
        **BaseObject._json_to_fields_mapping,
    }

    def __init__(
        self,
        id: str,
        display_name: str,
        level: int,
        *,
        parent_id: Optional[str] = None,
        node_path: Optional[List[str]] = None,
        ancestors: Optional[List[MetadataTaxonomyAncestor]] = None,
        **kwargs
    ):
        """
                :param id: A unique identifier of the metadata taxonomy node.
                :type id: str
                :param display_name: The display name of the metadata taxonomy node.
                :type display_name: str
                :param level: An index of the level to which the node belongs.
                :type level: int
                :param parent_id: The identifier of the parent node., defaults to None
                :type parent_id: Optional[str], optional
                :param node_path: An array of identifiers for all ancestor nodes.
        Not returned for root-level nodes., defaults to None
                :type node_path: Optional[List[str]], optional
                :param ancestors: An array of objects for all ancestor nodes.
        Not returned for root-level nodes., defaults to None
                :type ancestors: Optional[List[MetadataTaxonomyAncestor]], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.display_name = display_name
        self.level = level
        self.parent_id = parent_id
        self.node_path = node_path
        self.ancestors = ancestors
