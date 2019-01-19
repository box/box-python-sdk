# coding: utf-8
# pylint:disable=no-value-for-parameter

from __future__ import absolute_import, unicode_literals

from collections import OrderedDict
from itertools import chain
import sys

from enum import EnumMeta
from six import reraise
from six.moves import map   # pylint:disable=redefined-builtin


__all__ = list(map(str, ['ExtendableEnumMeta']))


class ExtendableEnumMeta(EnumMeta):
    """A metaclass for enum hierarchies.

    This allows you to define hierarchies such as this:

        from box.util.compat import with_metaclass

        class EnumBase(with_metaclass(ExtendableEnumMeta, Enum)): pass

        class Enum1(EnumBase):
            A = 'A'

        class Enum2(EnumBase): pass

        class Enum2_1(Enum2):
            B = 'B'

        class Enum2_2(Enum2):
            C = 'C'

    and have all members be accessible on EnumBase (as well as have all members
    of Enum2_1 and Enum2_2 be available on Enum2) as if they had been defined
    there.

    Non-leaf classes still may not have members directly defined on them, as
    with standard enums.

    Most of the usual enum magic methods are extended: __contains__, __dir__,
    __getitem__, __getattr__, __iter__, __len__, and __reversed__. Only __new__
    is not extended; instead, a new method `lookup` is provided. The
    __members__ property is also extended.
    """

    def lookup(cls, value):
        """Custom value lookup, which does recursive lookups on subclasses.

        If this is a leaf enum class with defined members, this acts the same
        as __new__().

        But if this is a base class with no defined members of its own, it
        tries doing a value lookup on all its subclasses until it finds the
        value.

        NOTE: Because of the implementation details of Enum, this must be a new
        classmethod, and can't be implemented as __new__() [1].

        [1] <https://docs.python.org/3.5/library/enum.html#finer-points>

        :param value:
            The value to look up. Can be a value, or an enum instance.
        :type value:
            `varies`
        :raises:
            :class:`ValueError` if the value isn't found anywhere.
        """
        try:
            return cls(value)
        except ValueError:
            exc_info = sys.exc_info()
            for subclass in cls.__subclasses__():
                try:
                    return subclass.lookup(value)
                except ValueError:
                    pass
            # This needs to be `reraise()`, and not just `raise`. Otherwise,
            # the inner exception from the previous line is re-raised, which
            # isn't desired.
            reraise(*exc_info)

    @property
    def __members__(cls):
        members = OrderedDict(super(ExtendableEnumMeta, cls).__members__)
        for subclass in cls.__subclasses__():
            members.update(subclass.__members__)
        return members

    def __contains__(cls, member):
        if super(ExtendableEnumMeta, cls).__contains__(member):
            return True

        def in_(subclass):
            return member in subclass

        return any(map(in_, cls.__subclasses__()))

    def __dir__(cls):
        return list(set(super(ExtendableEnumMeta, cls).__dir__()).union(*map(dir, cls.__subclasses__())))

    def __getitem__(cls, name):
        try:
            return super(ExtendableEnumMeta, cls).__getitem__(name)
        except KeyError:
            exc_info = sys.exc_info()
            for subclass in cls.__subclasses__():
                try:
                    return subclass[name]
                except KeyError:
                    pass
            # This needs to be `reraise()`, and not just `raise`. Otherwise,
            # the inner exception from the previous line is re-raised, which
            # isn't desired.
            reraise(*exc_info)

    def __getattr__(cls, name):
        try:
            return super(ExtendableEnumMeta, cls).__getattr__(name)
        except AttributeError:
            exc_info = sys.exc_info()
            try:
                # If the super() call fails, don't call getattr() on all of the
                # subclasses. Instead, use __getitem__ to do this. This is
                # because we don't want to grab arbitrary attributes from
                # subclasses, only enum members. For enum members, __getattr__
                # and __getitem__ have the same behavior. And __getitem__ has
                # the advantage of never grabbing anything other than enum
                # members.
                return cls[name]  # pylint:disable=unsubscriptable-object
            except KeyError:
                pass
            # This needs to be `reraise()`, and not just `raise`. Otherwise,
            # the inner exception from the previous line is re-raised, which
            # isn't desired.
            reraise(*exc_info)

    def __iter__(cls):
        return chain(super(ExtendableEnumMeta, cls).__iter__(), chain.from_iterable(map(iter, cls.__subclasses__())))

    def __len__(cls):
        return super(ExtendableEnumMeta, cls).__len__() + sum(map(len, cls.__subclasses__()))

    def __reversed__(cls):
        return reversed(list(cls))
