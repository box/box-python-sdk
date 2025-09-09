from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class CollectionTypeField(str, Enum):
    COLLECTION = 'collection'


class CollectionNameField(str, Enum):
    FAVORITES = 'Favorites'


class CollectionCollectionTypeField(str, Enum):
    FAVORITES = 'favorites'


class Collection(BaseObject):
    _discriminator = 'type', {'collection'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[CollectionTypeField] = None,
        name: Optional[CollectionNameField] = None,
        collection_type: Optional[CollectionCollectionTypeField] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for this collection., defaults to None
                :type id: Optional[str], optional
                :param type: The value will always be `collection`., defaults to None
                :type type: Optional[CollectionTypeField], optional
                :param name: The name of the collection., defaults to None
                :type name: Optional[CollectionNameField], optional
                :param collection_type: The type of the collection. This is used to
        determine the proper visual treatment for
        collections., defaults to None
                :type collection_type: Optional[CollectionCollectionTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.name = name
        self.collection_type = collection_type
