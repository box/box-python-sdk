import json

from typing import TYPE_CHECKING, Any, Union

from .base_object import BaseObject
from ..exception import BoxValueError
from ..util.api_call_decorator import api_call
from ..util.default_arg_value import SDK_VALUE_NOT_SET

if TYPE_CHECKING:
    from boxsdk.object.folder import Folder
    from boxsdk.object.collection import Collection


class BaseItem(BaseObject):

    @api_call
    def copy(self, *, parent_folder: 'Folder', name: str = None, **_kwargs) -> 'BaseItem':
        """Copy the item to the given folder.

        :param parent_folder:
            The folder to which the item should be copied.
        :param name:
            A new name for the item, in case there is already another item in the new parent folder with the same name.
        """
        self.validate_item_id(self._object_id)
        url = self.get_url('copy')
        data = {
            'parent': {'id': parent_folder.object_id}
        }
        if name is not None:
            data['name'] = name
        box_response = self._session.post(url, data=json.dumps(data))
        response = box_response.json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def move(self, parent_folder: 'Folder', name: str = None) -> 'BaseItem':
        """
        Move the item to the given folder.

        :param parent_folder:
            The parent `Folder` object, where the item will be moved to.
        :param name:
            A new name for the item, in case there is already another item in the new parent folder with the same name.
        """
        data = {
            'parent': {'id': parent_folder.object_id}
        }
        if name is not None:
            data['name'] = name
        return self.update_info(data=data)

    @api_call
    def rename(self, name: str) -> 'BaseItem':
        """
        Rename the item to a new name.

        :param name:
            The new name, you want the item to be renamed to.
        """
        data = {
            'name': name,
        }
        return self.update_info(data=data)

    @api_call
    def create_shared_link(self, **kwargs: Any) -> Any:
        """
        Create a shared link for the item with the given access permissions.

        :param kwargs:
            Keyword arguments passed from overriding method used to build request properties.
        :return:
            The updated object with shared link.
            Returns a new object of the same type, without modifying the original object passed as self.
        """
        shared_link = {}

        if kwargs.get('access') is not None:
            shared_link['access'] = kwargs.get('access')

        if kwargs.get('unshared_at') is not SDK_VALUE_NOT_SET:
            shared_link['unshared_at'] = kwargs.get('unshared_at')

        if kwargs.get('allow_download') is not None or kwargs.get('allow_preview') is not None:
            shared_link['permissions'] = {}
            if kwargs.get('allow_download') is not None:
                shared_link['permissions']['can_download'] = kwargs.get('allow_download')
            if kwargs.get('allow_preview') is not None:
                shared_link['permissions']['can_preview'] = kwargs.get('allow_preview')

        if kwargs.get('password') is not None:
            shared_link['password'] = kwargs.get('password')

        if kwargs.get('vanity_name') is not None:
            shared_link['vanity_name'] = kwargs.get('vanity_name')

        data = {'shared_link': shared_link}
        update_info_kwargs = {'etag': kwargs.get('etag')} if kwargs.get('etag') is not None else {}

        return self.update_info(data=data, **update_info_kwargs)

    @api_call
    def get_shared_link(self, **kwargs: Any) -> str:
        """
        Get a shared link for the item with the given access permissions.
        This url leads to a Box.com shared link page, where the item can be previewed, downloaded, etc.

        :param kwargs:
            Keyword arguments passed from overriding method used to create a new shared link.
        :returns:
            The URL of the shared link.
        """
        item = self.create_shared_link(**kwargs)
        return item.shared_link['url']  # pylint:disable=no-member

    @api_call
    def remove_shared_link(self, **kwargs: Any) -> bool:
        """
        Delete the shared link for the item.

        :param kwargs:
            Keyword arguments passed from overriding method used to build request properties.
        :returns:
            Whether or not the update was successful.
        """
        data = {'shared_link': None}
        update_info_kwargs = {'etag': kwargs.get('etag')} if kwargs.get('etag') is not None else {}

        item = self.update_info(data=data, **update_info_kwargs)
        return item.shared_link is None  # pylint:disable=no-member

    @api_call
    def add_to_collection(self, collection: 'Collection') -> 'BaseItem':
        """
        Add the item to a collection. This method is not currently safe from race conditions.

        :param collection:
            The collection to add the item to.
        :return:
            This item.
        """
        collections = self.get(fields=['collections']).collections  # pylint:disable=no-member
        collections.append({'id': collection.object_id})
        data = {
            'collections': collections
        }
        return self.update_info(data=data)

    @api_call
    def remove_from_collection(self, collection: 'Collection') -> 'BaseItem':
        """
        Remove the item from a collection.  This method is not currently safe from race conditions.

        :param collection:
            The collection to remove the item from.
        :return:
            This item.
        """
        collections = self.get(fields=['collections']).collections  # pylint:disable=no-member
        updated_collections = [c for c in collections if c['id'] != collection.object_id]
        data = {
            'collections': updated_collections
        }
        return self.update_info(data=data)

    @staticmethod
    def validate_item_id(item_id: Union[str, int]) -> None:
        """
        Validates an item ID is numeric

        :param item_id
        :raises:
            BoxException: if item_id is not numeric
        :returns:
        """
        if not isinstance(item_id, int) and not item_id.isdigit():
            raise BoxValueError("Invalid item ID")
