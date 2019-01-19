# coding: utf-8

from __future__ import unicode_literals
from datetime import datetime, timedelta
import pytest
from boxsdk.util.compat import with_metaclass


@pytest.fixture(params=(
    (timedelta(seconds=7), 7),
    (datetime(2015, 7, 6, 12) - datetime(2015, 7, 6, 11), 60 * 60),
    (timedelta(minutes=1), 60),
))
def total_seconds_data(request):
    return request.param


def test_total_seconds(total_seconds_data):
    # pylint:disable=redefined-outer-name
    delta, seconds = total_seconds_data
    assert delta.total_seconds() == seconds


def test_with_metaclass():

    class Class1(object):
        pass

    class Class2(object):
        pass

    bases = (Class1, Class2)

    class Meta(type):
        @classmethod
        def __prepare__(metacls, name, this_bases, **kwds):   # pylint:disable=unused-argument
            assert this_bases == bases
            return {}

        def __new__(metacls, name, this_bases, namespace, **kwds):
            assert this_bases == bases
            return super(Meta, metacls).__new__(metacls, name, this_bases, namespace, **kwds)

    temporary_class = with_metaclass(Meta, *bases)
    assert isinstance(temporary_class, Meta)
    assert temporary_class.__bases__ == bases

    class Subclass(temporary_class):
        pass

    assert type(Subclass) is Meta   # pylint:disable=unidiomatic-typecheck
    assert Subclass.__bases__ == bases
