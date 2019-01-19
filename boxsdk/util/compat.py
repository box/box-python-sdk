# coding: utf-8

from __future__ import absolute_import, division, unicode_literals

import six
from six.moves import map


NoneType = type(None)


def with_metaclass(meta, *bases, **with_metaclass_kwargs):
    """Extends the behavior of six.with_metaclass.

    The normal usage (expanded to include temporaries, to make the illustration
    easier) is:

    .. code-block:: python

        temporary_class = six.with_metaclass(meta, *bases)
        temporary_metaclass = type(temporary_class)

        class Subclass(temporary_class):
            ...

        SubclassMeta = type(Subclass)

    In this example:

    - ``temporary_class`` is a class with ``(object,)`` as its bases.
    - ``temporary_metaclass`` is a metaclass with ``(meta,)`` as its bases.
    - ``Subclass`` is a class with ``bases`` as its bases.
    - ``SubclassMeta`` is ``meta``.

    ``six.with_metaclass()`` is defined in such a way that it can make sure
    that ``Subclass`` has the correct metaclass and bases, while only using
    syntax which is common to both Python 2 and Python 3.
    ``temporary_metaclass()`` returns an instance of ``meta``, rather than an
    instance of itself / a subclass of ``temporary_class``, which is how
    ``SubclassMeta`` ends up being ``meta``, and how the temporaries don't
    appear anywhere in the final subclass.

    There are two problems with the current (as of six==1.10.0) implementation
    of ``six.with_metaclass()``, which this function solves.

    ``six.with_metaclass()`` does not define ``__prepare__()`` on the temporary
    metaclass. This means that ``meta.__prepare__()`` gets called directly,
    with bases set to ``(object,)``. If it needed to actually receive
    ``bases``, then errors might occur. For example, this was a problem when
    used with ``enum.EnumMeta`` in Python 3.6. Here we make sure that
    ``__prepare__()`` is defined on the temporary metaclass, and pass ``bases``
    to ``meta.__prepare__()``. This is fixed in six>=1.11.0 by PR #178 [1].

    Since ``temporary_class`` doesn't have the correct bases, in theory this
    could cause other problems, besides the previous one, in certain edge
    cases. To make sure that doesn't become a problem, we make sure that
    ``temporary_class`` has ``bases`` as its bases, just like the final class.

    [1] <https://github.com/benjaminp/six/pull/178>
    """
    temporary_class = six.with_metaclass(meta, *bases, **with_metaclass_kwargs)
    temporary_metaclass = type(temporary_class)

    class TemporaryMetaSubclass(temporary_metaclass, _most_derived_metaclass(meta, bases)):

        if '__prepare__' not in temporary_metaclass.__dict__:
            # six<1.11.0, __prepare__ is not defined on the temporary metaclass.

            @classmethod
            def __prepare__(mcs, name, this_bases, **kwds):  # pylint:disable=unused-argument,arguments-differ
                return meta.__prepare__(name, bases, **kwds)

    return type.__new__(TemporaryMetaSubclass, str('temporary_class'), bases, {})


def _most_derived_metaclass(meta, bases):
    """Selects the most derived metaclass of all the given metaclasses.

    This will be the same metaclass that is selected by

    .. code-block:: python

        class temporary_class(*bases, metaclass=meta): pass

    or equivalently by

    .. code-block:: python

        types.prepare_class('temporary_class', bases, metaclass=meta)

    "Most derived" means the item in {meta, type(bases[0]), type(bases[1]), ...}
    which is a non-strict subclass of every item in that set.

    If no such item exists, then :exc:`TypeError` is raised.

    :type meta:   `type`
    :type bases:  :class:`Iterable` of `type`
    """
    most_derived_metaclass = meta
    for base_type in map(type, bases):
        if issubclass(base_type, most_derived_metaclass):
            most_derived_metaclass = base_type
        elif not issubclass(most_derived_metaclass, base_type):
            # Raises TypeError('metaclass conflict: ...')
            return type.__new__(meta, str('temporary_class'), bases, {})
    return most_derived_metaclass
