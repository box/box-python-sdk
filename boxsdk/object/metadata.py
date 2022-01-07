# coding: utf-8

import json
from typing import TYPE_CHECKING, List, Any
from boxsdk.object.base_endpoint import BaseEndpoint
from boxsdk.exception import BoxAPIException
from ..util.api_call_decorator import api_call

if TYPE_CHECKING:
    from boxsdk.session.session import Session
    from boxsdk.object.base_object import BaseObject


class MetadataUpdate:
    """
    Helper class for updating Box metadata.
    See https://developer.box.com/en/guides/metadata/instances/update/ for more details.
    See http://jsonpatch.com/ for details about JSON patch.
    """
    def __init__(self):
        self._ops = []

    @property
    def ops(self) -> List[dict]:
        """
        Get a list of json patch operations in this update.

        :return:
            The list of json patch operations in this update.
        """
        return self._ops

    def add(self, path: str, value: str) -> None:
        """
        Insert an add operation to this metadata update.

        :param path:
            JSON pointer specifying where to add the new value.
        :param value:
            The value to add to the metadata document.
        """
        self._ops.append({'op': 'add', 'path': path, 'value': value})

    def remove(self, path: str, old_value: str = None) -> None:
        """
        Insert a remove operation to this metadata update.

        :param path:
            JSON pointer specifying where to remove the value from.
        :param old_value:
            If specified, only remove the key/value pair if the current value is equal to oldValue.
        """
        if old_value is not None:
            self._ops.append({'op': 'test', 'path': path, 'value': old_value})
        self._ops.append({'op': 'remove', 'path': path})

    def update(self, path: str, value: str, old_value: str = None) -> None:
        """
        Insert an update operation to this metadata update.

        :param path:
            JSON pointer specifying where the value is in the metadata document that should be updated.
        :param value:
            The updated value.
        :param old_value:
            If specified, only update the key/value pair if the current value is equal to oldValue.
        """
        if old_value is not None:
            self._ops.append({'op': 'test', 'path': path, 'value': old_value})
        self._ops.append({'op': 'replace', 'path': path, 'value': value})

    def test(self, path: str, value: str) -> None:
        """
        Insert a test operation to this metadata update.
        A test operation can invalidate the following operation if the value at the specified path does not match
        the supplied value.

        :param path:
            JSON pointer specifying where the value is in the metadata document to test.
        :param value:
            The value to match against.
        """
        self._ops.append({'op': 'test', 'path': path, 'value': value})


class Metadata(BaseEndpoint):
    def __init__(self, session: 'Session', box_object: 'BaseObject', scope: str, template: str):
        """
        :param session:
            The Box session used to make requests.
        :param box_object:
            The Box object this metadata instance will be associated with.
        :param scope:
            Scope of the metadata. Must be either 'global' or 'enterprise'.
        :param template:
            The name of the metadata template.
            See https://developer.box.com/en/guides/metadata/ for more details.
        """
        super().__init__(session)
        self._object = box_object
        self._scope = scope
        self._template = template

    def get_url(self, *args: Any) -> str:
        """ Base class override. """
        return self._object.get_url('metadata', self._scope, self._template)

    @staticmethod
    def start_update() -> MetadataUpdate:
        """
        Get a :class:`MetadataUpdate` for use with the :meth:`update` method.

        :return:
            A metadata update object that can be used to update this metadata object.
        """
        return MetadataUpdate()

    @api_call
    def update(self, metadata_update: MetadataUpdate) -> 'Metadata':
        """
        Update the key/value pairs associated with this metadata object.
        See https://developer.box.com/en/guides/metadata/instances/update/ for more details.

        :param metadata_update:
            A metadata update object containing the changes that should be made to the metadata.
        :return:
            A dictionary containing the updated key/value pairs for this metadata object.
        """
        return self._session.put(
            self.get_url(),
            data=json.dumps(metadata_update.ops),
            headers={b'Content-Type': b'application/json-patch+json'},
        ).json()

    @api_call
    def get(self) -> 'Metadata':
        """
        Get the key/value pairs that make up this metadata instance.

        :return:
            A dictionary containing the key/value pairs for this metadata object.
        """
        return self._session.get(self.get_url()).json()

    @api_call
    def delete(self) -> bool:
        """
        Delete the metadata object.

        :returns:
            Whether or not the delete was successful.
        """
        return self._session.delete(self.get_url()).ok

    @api_call
    def create(self, metadata: dict) -> 'Metadata':
        """
        Create the metadata instance on Box. If the instance already exists, use :meth:`update` instead.

        :param metadata:
            The key/value pairs to be stored in this metadata instance on Box.
        :return:
            A dictionary containing the key/value pairs for this metadata object.
        """
        return self._session.post(
            self.get_url(),
            data=json.dumps(metadata),
            headers={b'Content-Type': b'application/json'},
        ).json()

    @api_call
    def set(self, metadata: dict) -> 'Metadata':
        """
        Set the metadata instance on a :class:`Folder` or :class:`File`. Attempts to first create metadata on a
        :class:`Folder` or :class:`File`. If metadata already exists then attempt an update.

        :param metadata:
            The key/value pairs to be stored in this metadata instance on Box.
        :return:
            A dictionary containing the key/value pairs for this metadata object.
        """
        try:
            metadata_value = self.create(metadata)
        except BoxAPIException as err:
            if err.status == 409:
                updates = self.start_update()
                for key, value in metadata.items():
                    updates.add('/' + key, value)
                metadata_value = self.update(updates)
            else:
                raise
        return metadata_value

    def clone(self, session: 'Session' = None) -> 'Metadata':
        """ Base class override. """
        return self.__class__(session or self._session, self._object, self._scope, self._template)
