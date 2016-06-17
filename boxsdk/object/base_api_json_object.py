# coding: utf-8

from __future__ import unicode_literals
from abc import ABCMeta

import six

from boxsdk.util.translator import Translator


class BaseAPIJSONObjectMeta(ABCMeta):
    """
    Metaclass for Box API objects. Registers classes so that API responses can be translated to the correct type.
    Relies on the _item_type field defined on the classes to match the type property of the response json.
    But the type-class mapping will only be registered if the module of the class is imported.
    So it's also important to add the module name to __all__ in object/__init__.py.
    """
    def __init__(cls, name, bases, attrs):
        super(BaseAPIJSONObjectMeta, cls).__init__(name, bases, attrs)
        item_type = attrs.get('_item_type', None)
        if item_type is not None:
            Translator().register(item_type, cls)


@six.add_metaclass(BaseAPIJSONObjectMeta)
class BaseAPIJSONObject(object):
    """Base class containing basic logic shared between true REST objects and other objects (such as an Event)"""

    def __init__(self, object_id=None, response_object=None):
        self._object_id = object_id or ''
        self._response_object = response_object or {}
        self.__dict__.update(self._response_object)

    def __getitem__(self, item):
        """Base class override. Try to get the attribute from the API response object."""
        return self._response_object[item]

    def __repr__(self):
        """Base class override. Return a human-readable representation using the Box ID or name of the object."""
        description = '<Box {0} - {1}>'.format(self.__class__.__name__, self._description)
        if six.PY2:
            return description.encode('utf-8')
        else:
            return description

    @property
    def _description(self):
        if 'name' in self._response_object:
            return '{0} ({1})'.format(self._object_id, self.name)  # pylint:disable=no-member
        else:
            return '{0}'.format(self._object_id)

    @property
    def object_id(self):
        """Return the Box ID for the object.

        :rtype:
            `unicode`
        """
        return self._object_id

    def __eq__(self, other):
        """Base class override. Equality is determined by object id."""
        return self._object_id == other.object_id
