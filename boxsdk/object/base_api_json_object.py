# coding: utf-8

from __future__ import unicode_literals, absolute_import

import six

from ..util.translator import Translator


class BaseAPIJSONObjectMeta(type):
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

    def __init__(self, response_object=None):
        """
        :param response_object:
            The Box API response representing the object.
        :type response_object:
            :class:`BoxResponse`
        """
        self._response_object = response_object or {}
        self.__dict__.update(self._response_object)

    def __getitem__(self, item):
        """Base class override. Try to get the attribute from the API response object."""
        return self._response_object[item]

    def __repr__(self):
        """Base class override. Return a human-readable representation using the Box ID or name of the object."""
        extra_description = ' - {0}'.format(self._description) if self._description else ''
        description = '<Box {0}{1}'.format(self.__class__.__name__, extra_description)
        if six.PY2:
            return description.encode('utf-8')
        else:
            return description

    @property
    def _description(self):
        return ""
