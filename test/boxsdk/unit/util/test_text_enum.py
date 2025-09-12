from boxsdk.util.text_enum import TextEnum


class MockTextEnum(TextEnum):
    MEMBER = 'member'


def test_text_enum_repr_is_value():
    assert repr(MockTextEnum.MEMBER) == MockTextEnum.MEMBER.value


def test_text_enum_str_is_value():
    assert str(MockTextEnum.MEMBER) == str('member')
