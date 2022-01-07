# coding: utf-8

import copy
from typing import Any, Iterator, Iterable, Optional

from ..util.translator import Translator


class BaseAPIJSONObjectMeta(type):
    """
    Metaclass for Box API objects.

    Registers classes with the default translator, so that API responses can be
    translated to the correct type. This relies on the _item_type field, which
    must be defined in the class's namespace dict (and must be re-defined, in
    order to register a custom subclass), to match the 'type' field of the
    response json.  But the type-class mapping will only be registered if the
    module of the class is imported.

    For example, events returned from the API look like

    .. code-block:: json

        {'type': 'event', ...}

    so a class for that type could be created and registered with the default
    translator like this:

    .. code-block:: python

        class Event(BaseAPIJSONObject):
            _item_type = 'event'
            ...

    NOTE: The default translator registration functionality is a private
    implementation detail of the SDK, to make it easy to register the default
    API object classes with the default translator. For convenience and
    backwards-compatability, developers are allowed to re-define the _item_type
    field in their own custom subclasses in order to take advantage of this
    functionality, but are encouraged not to. Since this is a private
    implementation detail, it may change or be removed in any major or minor
    release. Additionally, it has the usual hazards of mutable global state.
    The supported and recommended ways for registering custom subclasses are:

    - Constructing a new :class:`Translator`, calling `Translator.register()`
      as necessary, and passing it to the :class:`BoxSession` constructor.
    - Calling `session.translator.register()` on an existing
      :class:`BoxSession`.
    - Calling `client.translator.register()` on an existing :class:`Client`.
    """

    def __init__(cls, name, bases, attrs):
        super(BaseAPIJSONObjectMeta, cls).__init__(name, bases, attrs)
        item_type = attrs.get('_item_type', None)
        if item_type is not None:
            Translator._default_translator.register(item_type, cls)   # pylint:disable=protected-access,no-member
            # Some types have - in them instead of _ in the API.
            if "-" in item_type:
                Translator._default_translator.register(item_type.replace("-", "_"), cls)   # pylint:disable=protected-access,no-member


class BaseAPIJSONObject(metaclass=BaseAPIJSONObjectMeta):
    """Base class containing basic logic shared between true REST objects and other objects (such as an Event)"""

    # :attr _item_type:
    #     (protected) The Box resource type that this class represents.
    #     For API object/resource classes this should equal the expected value
    #     of the 'type' field in API JSON responses. Otherwise, this should be
    #     `None`.
    #
    # NOTE: When defining a leaf class with an _item_type in this SDK, it's
    # also important to add the module name to __all__ in object/__init__.py,
    # so that it will be imported and registered with the default translator.
    _item_type: Optional[str] = None
    _untranslated_fields = ()

    def __init__(self, response_object: dict = None, **kwargs: Any):
        """
        :param response_object:
            A JSON object representing the object returned from a Box API request.
        """
        super().__init__(**kwargs)
        self._response_object = response_object or {}
        self.__dict__.update(self._response_object)

    def __getitem__(self, item: str) -> Any:
        """
        Try to get the attribute from the API response object.

        :param item:
            The attribute to retrieve from the API response object.
        """
        return self._response_object[item]

    def __contains__(self, item: str) -> bool:
        """
        Does the response object contains this item attribute?

        :param item:
            The attribute to check for in the API response object.

        """
        return item in self._response_object

    def __iter__(self) -> Iterator:
        """
        Get all of the keys of the API response object.
        """
        return iter(self._response_object)

    def __repr__(self) -> str:
        """Base class override. Return a human-readable representation using the Box ID or name of the object."""
        extra_description = f' - {self._description}' if self._description else ''
        description = f'<Box {self.__class__.__name__}{extra_description}>'
        return description

    @property
    def _description(self) -> str:
        """Return a description of the object if one exists."""
        return ""

    @property
    def object_type(self) -> str:
        """Return the Box type for the object.
        """
        return self._item_type

    @classmethod
    def untranslated_fields(cls) -> tuple:
        """
        The fields that should not be translated on this object.
        """
        return cls._untranslated_fields

    @classmethod
    def _untranslate(cls, value: Any) -> Iterable:
        """
        Untranslates a given object into a dictionary.

        :param value:
            The object to untranslate.
        :return:
            A dictionary containing the untranslated object.
        """
        if isinstance(value, BaseAPIJSONObject):
            return cls._untranslate(value._response_object)  # pylint:disable=protected-access
        if isinstance(value, dict):
            return {k: cls._untranslate(v) for (k, v) in value.items()}
        if isinstance(value, list):
            return [cls._untranslate(entry) for entry in value]

        return copy.copy(value)

    @property
    def response_object(self) -> Iterable:
        """
        Return the JSON object representing the object returned from a Box API request.
        """
        return self._untranslate(self)
