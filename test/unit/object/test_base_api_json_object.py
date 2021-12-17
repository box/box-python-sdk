# coding: utf-8

import pytest

from boxsdk.object.base_api_json_object import BaseAPIJSONObject
from boxsdk.object.base_object import BaseObject
from boxsdk.object.folder import Folder


@pytest.fixture(params=[{'foo': 'bar'}, {'a': {'b': 'c'}}])
def response(request):
    return request.param


@pytest.fixture()
def base_api_json_object(response):
    dictionary_response = response
    return dictionary_response, BaseAPIJSONObject(dictionary_response)


def test_getitem(base_api_json_object):
    dictionary_response, test_object = base_api_json_object
    assert isinstance(test_object, BaseAPIJSONObject)
    for key in dictionary_response:
        assert test_object[key] == dictionary_response[key]


def test_contains(base_api_json_object):
    dictionary_response, test_object = base_api_json_object
    for key in dictionary_response:
        assert key in test_object
    assert 'some_key_that_doesnt_exist' not in test_object


def test_iter(base_api_json_object):
    dictionary_response, test_object = base_api_json_object
    all_test_object_keys = list(test_object)
    all_dictionary_response_keys = list(dictionary_response)
    assert set(all_test_object_keys) == set(all_dictionary_response_keys)


def test_meta_registers_new_item_type_in_default_translator(default_translator, original_default_translator):
    item_type = u'ƒøø'

    class Foo(BaseAPIJSONObject):
        _item_type = item_type

    assert default_translator.get(item_type) is Foo
    assert (set(default_translator) - set(original_default_translator)) == set([item_type])


@pytest.mark.parametrize('subclass', [BaseAPIJSONObject, BaseObject, Folder])
def test_meta_does_not_register_new_subclass_in_default_translator_if_item_type_is_not_defined_in_namespace(
        subclass,
        default_translator,
        original_default_translator,
):

    class Foo(subclass):
        pass

    assert Foo not in default_translator.values()
    assert default_translator == original_default_translator


def test_meta_overrides_registration_if_subclass_redefines_item_type(default_translator, original_default_translator):

    class FolderSubclass(Folder):
        _item_type = 'folder'

    assert default_translator.get('folder') is FolderSubclass
    assert set(default_translator.keys()) == set(original_default_translator.keys())
