# coding: utf-8

import pytest

from boxsdk.object.api_json_object import APIJSONObject


@pytest.fixture(params=[{'foo': 'bar'}, {'a': {'b': 'c'}}])
def api_json_object(request):
    return request.param, APIJSONObject(request.param)


def test_len(api_json_object):
    dictionary, test_object = api_json_object
    assert len(dictionary) == len(test_object)


def test_api_json_object_dict(api_json_object):
    dictionary, test_object = api_json_object
    assert dictionary == test_object
