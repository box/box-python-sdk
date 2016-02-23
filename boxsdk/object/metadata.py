# coding: utf-8

from __future__ import unicode_literals
import json
from boxsdk.object.base_endpoint import BaseEndpoint


class MetadataUpdate(object):
    """
    Helper class for updating Box metadata.
    See https://box-content.readme.io/reference#update-metadata for more details.
    See http://jsonpatch.com/ for details about JSON patch.
    """
    def __init__(self):
        self._ops = []

    @property
    def ops(self):
        """
        Get a list of json patch operations in this update.

        :return:
            The list of json patch operations in this update.
        :rtype:
            `list` of `dict`
        """
        return self._ops

    def add(self, path, value):
        """
        Insert an add operation to this metadata update.

        :param path:
            JSON pointer specifying where to add the new value.
        :type path:
            `unicode`
        :param value:
            The value to add to the metadata document.
        :type value:
            `unicode`
        """
        self._ops.append({'op': 'add', 'path': path, 'value': value})

    def remove(self, path, old_value=None):
        """
        Insert a remove operation to this metadata update.

        :param path:
            JSON pointer specifying where to remove the value from.
        :type path:
            `unicode`
        :param old_value:
            If specified, only remove the key/value pair if the current value is equal to oldValue.
        :type old_value:
            `unicode`
        """
        if old_value is not None:
            self._ops.append({'op': 'test', 'path': path, 'value': old_value})
        self._ops.append({'op': 'remove', 'path': path})

    def update(self, path, value, old_value=None):
        """
        Insert an update operation to this metadata update.

        :param path:
            JSON pointer specifying where the value is in the metadata document that should be updated.
        :type path:
            `unicode`
        :param value:
            The updated value.
        :type value:
            `unicode`
        :param old_value:
            If specified, only update the key/value pair if the current value is equal to oldValue.
        :type old_value:
            `unicode`
        """
        if old_value is not None:
            self._ops.append({'op': 'test', 'path': path, 'value': old_value})
        self._ops.append({'op': 'replace', 'path': path, 'value': value})

    def test(self, path, value):
        """
        Insert a test operation to this metadata update.
        A test operation can invalidate the following operation if the value at the specified path does not match
        the supplied value.

        :param path:
            JSON pointer specifying where the value is in the metadata document to test.
        :type path:
            `unicode`
        :param value:
            The value to match against.
        :type value:
            `unicode`
        """
        self._ops.append({'op': 'test', 'path': path, 'value': value})


class Metadata(BaseEndpoint):
    def __init__(self, session, box_object, scope, template):
        """
        :param session:
            The Box session used to make requests.
        :type session:
            :class:`BoxSession`
        :param box_object:
            The Box object this metadata instance will be associated with.
        :type box_object:
            :class:`BaseObject`
        :param scope:
            Scope of the metadata. Must be either 'global' or 'enterprise'.
        :type scope:
            `unicode`
        :param template:
            The name of the metadata template.
            See https://box-content.readme.io/reference#metadata-object for more details.
        :type template:
            `unicode`
        """
        super(Metadata, self).__init__(session)
        self._object = box_object
        self._scope = scope
        self._template = template

    def get_url(self, *args):
        """ Base class override. """
        return self._object.get_url('metadata', self._scope, self._template)

    @staticmethod
    def start_update():
        """
        Get a :class:`MetadataUpdate` for use with the :meth:`update` method.

        :return:
            A metadata update object that can be used to update this metadata object.
        :rtype:
            :class:`MetadataUpdate`
        """
        return MetadataUpdate()

    def update(self, metadata_update):
        """
        Update the key/value pairs associated with this metadata object.
        See https://box-content.readme.io/reference#update-metadata for more details.

        :param metadata_update:
            A metadata update object containing the changes that should be made to the metadata.
        :type metadata_update:
            :class:`MetadataUpdate`
        :return:
            A dictionary containing the updated key/value pairs for this metadata object.
        :rtype:
            :class:`Metadata`
        """
        return self._session.put(
            self.get_url(),
            data=json.dumps(metadata_update.ops),
            headers={b'Content-Type': b'application/json-patch+json'},
        ).json()

    def get(self):
        """
        Get the key/value pairs that make up this metadata instance.

        :return:
            A dictionary containing the key/value pairs for this metadata object.
        :rtype:
            :class:`Metadata`
        """
        return self._session.get(self.get_url()).json()

    def delete(self):
        """
        Delete the metadata object.

        :returns:
            Whether or not the delete was successful.
        :rtype:
            `bool`
        """
        return self._session.delete(self.get_url()).ok

    def create(self, metadata):
        """
        Create the metadata instance on Box. If the instance already exists, use :meth:`update` instead.

        :param metadata:
            The key/value pairs to be stored in this metadata instance on Box.
        :type metadata:
            `dict`
        :return:
            A dictionary containing the key/value pairs for this metadata object.
        :rtype:
            :class:`Metadata`
        """
        return self._session.post(
            self.get_url(),
            data=json.dumps(metadata),
            headers={b'Content-Type': b'application/json'},
        ).json()

    def as_user(self, user):
        """ Base class override. """
        return self.__class__(self._session.as_user(user), self._object, self._scope, self._template)

    def with_shared_link(self, shared_link, shared_link_password):
        """ Base class override. """
        return self.__class__(
            self._session.with_shared_link(shared_link, shared_link_password),
            self._object,
            self._scope,
            self._template
        )
