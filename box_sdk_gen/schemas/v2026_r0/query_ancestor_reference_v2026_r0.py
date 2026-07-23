from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class QueryAncestorReferenceV2026R0(BaseObject):
    def __init__(self, id: str, type: str, **kwargs):
        """
        :param id: The unique identifier of the ancestor entity.
        :type id: str
        :param type: The type of the ancestor entity. Possible value: folder.
        :type type: str
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
