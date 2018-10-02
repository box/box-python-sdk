# coding: utf-8

from __future__ import absolute_import, unicode_literals

import inspect

from .chain_map import ChainMap


__all__ = list(map(str, ['Translator']))


def _get_object_id(obj):
    """
    Gets the ID for an API object.

    :param obj:
        The API object
    :type obj:
        `dict`
    :return:
    """
    if obj.get('type', '') == 'event':
        return obj.get('event_id', None)

    return obj.get('id', None)


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

    def translate(self, session, response_object):
        """
        Translate a given API response object into SDK classes, rescursively translating any subobjects.

        :param session:
            The SDK session to use for any objects that require a session (i.e. classes that make API calls)
        :type session:
            class:`Session`
        :param response_object:
            The JSON response object from the API, which will be translated
        :type response_object:
            `dict`
        :return:
            The translated object
        """

        if isinstance(response_object, dict):
            for key in response_object:
                if isinstance(response_object[key], dict):
                    response_object[key] = self.translate(session, response_object[key])
                elif isinstance(response_object[key], list):
                    response_object[key] = [self.translate(session, o) for o in response_object[key]]

            # Try to translate any API object with a `type` property, except for metadata instances
            # The $type value in metadata instances isn't directly usable, so we avoid it altogether
            # NOTE: Currently, we represent metadata as just a `dict`, so there's no need to translate it anyway
            if 'type' in response_object and '$type' not in response_object:
                object_class = self.get(response_object.get('type', ''))
                param_values = {
                    'session': session,
                    'response_object': response_object,
                    'object_id': _get_object_id(response_object),
                }
                # NOTE: getargspec() is deprecated, and should be replaced by inspect.signature() when 2.7 support drops
                params = inspect.getargspec(object_class.__init__).args
                param_values = {p: param_values[p] for p in params if p != 'self'}
                return object_class(**param_values)

        return response_object


Translator._default_translator = Translator(extend_default_translator=False)  # pylint:disable=protected-access
