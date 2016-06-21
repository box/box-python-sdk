# coding: utf-8

from __future__ import unicode_literals, absolute_import
import pytest

from boxsdk.object.base_api_json_object import BaseAPIJSONObject


@pytest.fixture(params=[{'foo': 'bar'}, {'a': {'b': 'c'}}])
def base_api_json_object(request):
    return request.param, BaseAPIJSONObject(request.param)


def test_getitem(base_api_json_object):
    dictionary, test_object = base_api_json_object
    assert isinstance(test_object, BaseAPIJSONObject)
    for key in dictionary:
        assert test_object[key] == dictionary[key]
