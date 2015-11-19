# coding: utf-8

from __future__ import unicode_literals, absolute_import

from mock import Mock
import pytest

from boxsdk.util.api_response_decorator import api_response


@pytest.fixture
def mock_response():
    return Mock()


@pytest.fixture
def mock_object_class(mock_response):
    class MockObject(object):
        _translator_called = False
        _mock_response = mock_response

        @api_response
        def func(self, *args, **kwargs):
            # pylint:disable=unused-argument, no-self-use
            return self._mock_response

        @func.translator
        def func_translator_side_effect(self, response):
            assert response is self._mock_response
            self._translator_called = True
            return response

    return MockObject


@pytest.fixture
def mock_object(mock_object_class):
    return mock_object_class()


def test_api_response_decorator_calls_translator(mock_response, mock_object):
    args = (Mock(),)
    kwargs = {'foo': Mock()}

    response = mock_object.func(*args, **kwargs)

    assert response is mock_response
    assert response.args == args
    assert response.kwargs == kwargs


def test_api_response_decorator_works_when_called_on_class(mock_response, mock_object, mock_object_class):
    args = (mock_object, Mock(),)
    kwargs = {'foo': Mock()}

    response = mock_object_class.func(*args, **kwargs)

    assert response is mock_response
    assert response.args == args
    assert response.kwargs == kwargs


def test_api_response_decorator_works_when_none_is_returned_from_func(mock_object_class):
    class MockObjectNoResponse(mock_object_class):
        _mock_response = None

    mock_object = MockObjectNoResponse()

    response = mock_object.func()  # pylint:disable=no-member
    assert response is None
