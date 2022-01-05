# coding: utf-8

from boxsdk.util.text_enum import TextEnum


class MockTextEnum(TextEnum):
    MEMBER = 'member'


def test_text_enum_repr_is_value():
    assert MockTextEnum.MEMBER.__repr__() == MockTextEnum.MEMBER.value  # pylint:disable=no-member


def test_text_enum_str_is_value():
    assert str(MockTextEnum.MEMBER) == str('member')
