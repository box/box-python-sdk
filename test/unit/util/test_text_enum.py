# coding: utf-8

from __future__ import unicode_literals
from boxsdk.util.text_enum import TextEnum


class MockTextEnum(TextEnum):
    member = 'member'


def test_text_enum_repr_is_value():
    assert MockTextEnum.member.__repr__() == MockTextEnum.member.value  # pylint:disable=no-member


def test_text_enum_str_is_value():
    assert str(MockTextEnum.member) == str('member')
