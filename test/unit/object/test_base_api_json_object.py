# coding: utf-8

from __future__ import unicode_literals, absolute_import
import pytest

from boxsdk.object.base_api_json_object import BaseAPIJSONObject
from boxsdk.object.base_object import BaseObject
from boxsdk.object.folder import Folder
from boxsdk.util.translator import Translator


@pytest.fixture(params=[{'foo': 'bar'}, {'a': {'b': 'c'}}])
def response(request):
    return request.param


@pytest.fixture()
def default_translator():
    return Translator()

@pytest.fixture()
def original_default_translator():
    return Translator()


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
    all_test_object_keys = [key for key in test_object]
    all_dictionary_response_keys = [key for key in dictionary_response]
    assert set(all_test_object_keys) == set(all_dictionary_response_keys)


def test_meta_registers_new_item_type_in_default_translator(default_translator):
    item_type = u'ƒøø'

    class Foo(BaseAPIJSONObject):
        _item_type = item_type

    assert default_translator.translate(item_type) is Foo


def test_meta_overrides_registration_if_subclass_redefines_item_type(default_translator):

    class FolderSubclass(Folder):
        _item_type = 'folder'

    assert default_translator.translate('folder') is FolderSubclass
