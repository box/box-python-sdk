# coding: utf-8

from __future__ import absolute_import, unicode_literals

from enum import Enum
import pytest
from six import with_metaclass

from boxsdk.util.enum import ExtendableEnumMeta
from boxsdk.util.ordered_dict import OrderedDict


# pylint:disable=invalid-name
# So that we can have class definitions as pytest function fixtures.


@pytest.fixture(scope='function')
def EnumBase():

    class EnumBase(with_metaclass(ExtendableEnumMeta, Enum)):
        pass

    return EnumBase


@pytest.fixture(scope='function')
def Enum1(EnumBase):

    class Enum1(EnumBase):
        A = 1

    return Enum1


@pytest.fixture(scope='function')
def Enum2(EnumBase):

    class Enum2(EnumBase):
        pass

    return Enum2


@pytest.fixture(scope='function')
def Enum2_1(Enum2):

    class Enum2_1(Enum2):
        B = 2

    return Enum2_1


@pytest.fixture(scope='function')
def Enum2_2(Enum2):

    class Enum2_2(Enum2):
        C = 3

    return Enum2_2


@pytest.fixture(scope='function')
def EnumBaseWithSubclassesDefined(EnumBase, Enum1, Enum2_1, Enum2_2):   # pylint:disable=unused-argument
    return EnumBase


enum_member_names = ['A', 'B', 'C']
enum_member_values = [1, 2, 3]


@pytest.fixture(scope='session', params=enum_member_names)
def enum_member_name(request):
    return request.param


@pytest.fixture(scope='session', params=enum_member_values)
def enum_member_value(request):
    return request.param


@pytest.fixture(scope='function')
def enum_members(Enum1, Enum2_1, Enum2_2):
    members = OrderedDict()
    for enum_member_name, enum_class in zip(enum_member_names, [Enum1, Enum2_1, Enum2_2]):
        members[enum_member_name] = enum_class[enum_member_name]
    return members


@pytest.fixture(scope='function')
def enum_instance(enum_member_name, enum_members):
    return enum_members[enum_member_name]


def test_can_construct_enum_hierarchy(EnumBaseWithSubclassesDefined):   # pylint:disable=unused-argument
    pass


def test_can_not_construct_non_leaf_enum_with_members(Enum1):
    with pytest.raises(TypeError):
        class Enum1_1(Enum1):   # pylint:disable=unused-variable
            pass


def test_lookup(EnumBaseWithSubclassesDefined, enum_member_value):
    EnumBase = EnumBaseWithSubclassesDefined
    enum_instance = EnumBase.lookup(enum_member_value)
    assert isinstance(enum_instance, EnumBase)
    assert EnumBase.lookup(enum_instance) == enum_instance
    assert enum_instance.__class__.lookup(enum_instance) == enum_instance
    assert enum_instance.__class__(enum_instance) == enum_instance
    assert enum_instance.__class__(enum_member_value) == enum_instance


def test_lookup_raises_value_error_for_non_members(EnumBaseWithSubclassesDefined):
    with pytest.raises(ValueError):
        EnumBaseWithSubclassesDefined.lookup('foobar')


def test_members(EnumBaseWithSubclassesDefined, enum_members):
    assert dict(EnumBaseWithSubclassesDefined.__members__) == enum_members


def test_contains_enum_instances(EnumBaseWithSubclassesDefined, enum_instance):
    assert enum_instance in EnumBaseWithSubclassesDefined


def test_contains_returns_false_for_non_instances(EnumBaseWithSubclassesDefined, enum_member_name):
    assert enum_member_name not in EnumBaseWithSubclassesDefined


def test_getitem(EnumBaseWithSubclassesDefined, enum_member_name, enum_instance):
    assert EnumBaseWithSubclassesDefined[enum_member_name] == enum_instance


def test_getitem_raises_key_error_for_non_member_names(EnumBaseWithSubclassesDefined, enum_member_value):
    with pytest.raises(KeyError):
        EnumBaseWithSubclassesDefined[enum_member_value]  # pylint:disable=pointless-statement


def test_getattr(EnumBaseWithSubclassesDefined, enum_member_name, enum_instance):
    assert getattr(EnumBaseWithSubclassesDefined, enum_member_name) == enum_instance


def test_getattr_raises_attribute_error_for_non_member_names(EnumBaseWithSubclassesDefined):
    with pytest.raises(AttributeError):
        EnumBaseWithSubclassesDefined.foobar  # pylint:disable=pointless-statement


def test_getattr_does_get_arbitrary_attributes_from_itself(EnumBaseWithSubclassesDefined):
    EnumBase = EnumBaseWithSubclassesDefined
    EnumBase.foobar = 'foobar'
    assert EnumBase.foobar == 'foobar'


def test_getattr_does_not_get_arbitrary_attributes_from_subclasses(EnumBaseWithSubclassesDefined, Enum1):
    Enum1.foobar = 'foobar'
    with pytest.raises(AttributeError):
        EnumBaseWithSubclassesDefined.foobar  # pylint:disable=pointless-statement


def test_iter(EnumBaseWithSubclassesDefined, enum_members):
    assert list(EnumBaseWithSubclassesDefined) == list(enum_members.values())


def test_len(EnumBaseWithSubclassesDefined, enum_members):
    assert len(EnumBaseWithSubclassesDefined) == len(enum_members)


def test_reversed(EnumBaseWithSubclassesDefined):
    EnumBase = EnumBaseWithSubclassesDefined
    assert list(reversed(list(reversed(EnumBase)))) == list(EnumBase)
