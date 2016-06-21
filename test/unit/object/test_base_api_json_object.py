# coding: utf-8

from __future__ import unicode_literals, absolute_import
import pytest

from boxsdk.object.base_api_json_object import BaseAPIJSONObject


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
