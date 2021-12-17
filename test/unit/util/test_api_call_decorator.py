# coding: utf-8

from mock import NonCallableMock
import pytest

from boxsdk.object.cloneable import Cloneable
from boxsdk.util.api_call_decorator import api_call


@pytest.fixture
def api_call_result():
    return {'bar': 'ƒøø'}


@pytest.fixture(name='api_call_method')
def api_call_method_fixture(api_call_result):

    @api_call
    def api_call_method(self, *args, **kwargs):
        return self, args, kwargs, api_call_result

    return api_call_method


@pytest.fixture
def cloneable_subclass_with_api_call_method(api_call_method):
    api_call_method_fixture = api_call_method

    # pylint:disable=abstract-method
    class CloneableSubclass(Cloneable):
        api_call_method = api_call_method_fixture

    return CloneableSubclass


@pytest.fixture
def mock_cloneable(cloneable_subclass_with_api_call_method):

    # pylint:disable=abstract-method
    class MockCloneable(cloneable_subclass_with_api_call_method, NonCallableMock):
        pass

    return MockCloneable(spec_set=cloneable_subclass_with_api_call_method, name='Cloneable')


def test_api_call_is_decorator():

    @api_call
    def func():
        pass

    assert callable(func)
    assert hasattr(func, '__get__')


def test_api_call_decorated_function_must_be_a_method():

    @api_call
    def func():
        pass

    with pytest.raises(TypeError):
        func()


def test_api_call_decorated_method_must_be_a_cloneable_method():

    class NonCloneable:
        @api_call
        def func(self):
            pass

    obj = NonCloneable()
    with pytest.raises(TypeError):
        obj.func()


def test_api_call_decorated_method_must_be_bound_to_an_instance_of_the_owner(mock_cloneable, api_call_method):
    # pylint:disable=abstract-method
    class CloneableSubclass2(Cloneable):
        pass

    with pytest.raises(TypeError):
        api_call_method.__get__(mock_cloneable, CloneableSubclass2)


def test_api_call_decorated_method_returns_itself_when_bound_to_none(api_call_method, cloneable_subclass_with_api_call_method):
    assert api_call_method.__get__(None, Cloneable) is api_call_method
    assert not hasattr(api_call_method.__get__(None, Cloneable), '__self__')
    assert cloneable_subclass_with_api_call_method.api_call_method is api_call_method
    assert not hasattr(cloneable_subclass_with_api_call_method.api_call_method, '__self__')


def test_api_call_decorated_method_binds_to_instance(mock_cloneable, api_call_method):
    assert api_call_method.__get__(mock_cloneable, Cloneable) is not api_call_method
    assert api_call_method.__get__(mock_cloneable, Cloneable).__self__ is mock_cloneable
    assert mock_cloneable.api_call_method is not api_call_method
    assert mock_cloneable.api_call_method.__self__ is mock_cloneable


def test_api_call_decorated_method_delegates_to_wrapped_method(mock_cloneable, api_call_result):
    args = (1, 2, 'ƒøø', 'bar')
    kwargs = {'bar': 'ƒøø'}
    assert mock_cloneable.api_call_method(*args, **kwargs) == (mock_cloneable, args, kwargs, api_call_result)


def test_api_call_decorated_method_can_be_called_as_an_unbound_method_with_an_instance_as_the_first_argument(
        mock_cloneable,
        api_call_result,
        cloneable_subclass_with_api_call_method,
):
    args = (1, 2, 'ƒøø', 'bar')
    kwargs = {'bar': 'ƒøø'}
    api_call_method = cloneable_subclass_with_api_call_method.api_call_method
    assert api_call_method(mock_cloneable, *args, **kwargs) == (mock_cloneable, args, kwargs, api_call_result)
