# coding: utf-8

from __future__ import absolute_import, unicode_literals

from collections import Mapping
import inspect

from .chain_map import ChainMap


__all__ = list(map(str, ['Translator']))


class Translator(ChainMap):
    """
    Translate item responses from the Box API to Box objects.

    Also acts as a :class:`Mapping` from type names to Box object classes.

    There exists a global default `Translator`, containing the default API
    object classes defined by the SDK. Custom `Translator` instances can be
    created to extend the default `Translator` with custom subclasses.

    A `Translator` is a :class:`ChainMap`, so that one translator can "extend"
    others. The most common scenario would be a custom, non-global
    `Translator` that extends only the default translator, to register 0 or
    more new classes. But more complex inheritance is also allowed, in case
    that is useful.
    """

    __slots__ = ()

    # :attr _default_translator:
    #     A global `Translator` containing the default API object classes
    #     defined by the SDK. By default, new `Translator` instances will
    #     "extend" this one, so that the global registrations are reflected
    #     automatically.
    #
    #     NOTE: For convenience and backwards-compatability, developers are
    #     allowed to register their own custom subclasses with
    #     `_default_translator`, but are encouraged not to. The default
    #     translator may change or be removed in any major or minor release.
    #     Additionally, it has the usual hazards of mutable global state.
    #     The supported and recommended ways for registering custom subclasses
    #     are:
    #
    #     - Constructing a new `Translator`, calling `Translator.register()` as
    #     necessary, and passing it to the `BoxSession` constructor.
    #     - Calling `session.translator.register()` on an existing
    #     `BoxSession`.
    #     - Calling `client.translator.register()` on an existing `Client`.
    # :type _default_translator:   :class:`Translator`
    _default_translator = {}   # Will be set to a `Translator` instance below, after the class is defined.

    def __init__(self, *translation_maps, **kwargs):
        """Baseclass override.

        :param translation_maps:
            (variadic) The same as the `maps` variadic parameter to
            :class:`ChainMap`, except restricted to maps from type names to Box
            object classes.
        :type translation_maps:
            `tuple` of (:class:`Mapping` of `unicode` to :class:`BaseAPIJSONObjectMeta`)
        :param extend_default_translator:
            (optional, keyword-only) If `True` (the default),
            `_default_translator` is appended to the end of `translation_maps`.
            When this functionality is used, the new `Translator` will inherit
            all of the global registrations.
        :type extend_default_translator:  `bool`
        :param new_child:
            (optional, keyword-only) If `True` (the default), a new empty
            `dict` is prepended to the front of `translation_maps`. Either way,
            the resulting `Translator` starts out with the same key-value
            pairs. But when this is `False`, the first item in
            `translation_maps` will be mutated by `__setitem__()` and
            `__delitem()__` calls, which will affect other references to it.
            Whereas when this is `True`, all items in `translation_maps` are
            safe from mutation in normal usage scenarios.
        :type new_child:  `bool`
        """
        translation_maps = list(translation_maps)
        extend_default_translator = kwargs.pop('extend_default_translator', True)
        new_child = kwargs.pop('new_child', True)
        if extend_default_translator:
            translation_maps.append(self._default_translator)
        if new_child:
            translation_maps.insert(0, {})
        super(Translator, self).__init__(*translation_maps, **kwargs)

    def register(self, type_name, box_cls):
        """Associate a Box object class to handle Box API item responses with the given type name.

        :param type_name:
            The type name to be registered.
        :type type_name:
            `unicode`
        :param box_cls:
            The Box object class, which will be associated with the type name provided.
        :type box_cls:
            :class:`BaseAPIJSONObjectMeta`
        """
        self[type_name] = box_cls

    def get(self, key, default=None):
        """Get the box object class associated with the given type name.

        :param key:
            The type name to be translated.
        :type key:
            `unicode`
        :param default:
            (optional) The default Box object class to return.
            Defaults to `BaseObject`.
        :type default:  :class:`BaseAPIJSONObjectMeta`
        :rtype:   :class:`BaseAPIJSONObjectMeta`
        """
        from boxsdk.object.base_object import BaseObject
        if default is None:
            default = BaseObject
        return super(Translator, self).get(key, default)

    def translate(self, type_name):
        """
        Get the box object class associated with the given type name.

        :param type_name:
            The type name to be translated.
        :type type_name:
            `unicode`
        :rtype:   :class:`BaseAPIJSONObjectMeta`
        """
        return self.get(type_name)

    def full_translate(self, response_object, session):

        if isinstance(response_object, Mapping) and 'type' in response_object:
            object_type = response_object['type']
            object_id = response_object['event_id'] if object_type == 'event' else response_object['id']
            for key in response_object:
                if isinstance(response_object[key], Mapping):
                    response_object[key] = self.full_translate(response_object[key], session)
                elif isinstance(response_object, list):
                    for i in len(response_object[key]):
                        response_object[key][i] = self.full_translate(response_object[key][i], session)

            object_class = self.get(object_type)
            param_values = {
                'session': session,
                'response_object': response_object,
                'object_id': object_id,
            }
            params = inspect.signature(object_class.__init__).parameters
            param_values = {p:param_values[p] for p in params if self._is_constructor_param(params[p])}
            return self.get(object_type)(**param_values)

        return response_object

    def _is_constructor_param(self, param):
        if param.name is 'self':
            return False

        if param.kind is not param.POSITIONAL_OR_KEYWORD:
            return False

        return True


Translator._default_translator = Translator(extend_default_translator=False)  # pylint:disable=protected-access
