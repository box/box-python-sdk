# coding: utf-8

from __future__ import unicode_literals
from threading import Event, Thread
import pytest
from six import add_metaclass
from boxsdk.util.singleton import Singleton

# pylint:disable=redefined-outer-name


@pytest.fixture
def singleton_class():
    @add_metaclass(Singleton)
    class MySingleton(object):
        def __init__(self, on_enter=None, block_on=None):
            if on_enter:
                on_enter.set()
            if block_on:
                block_on.wait()
    return MySingleton


@pytest.fixture
def nested_singleton(singleton_class):
    @add_metaclass(Singleton)
    class Nested(object):
        def __init__(self):
            self.single = singleton_class()
    return Nested


def test_singleton_returns_singleton(singleton_class):
    instance1 = singleton_class()
    instance2 = singleton_class()

    assert instance1 is instance2


def test_nested_singletons_are_safely_initialized(nested_singleton, singleton_class):
    """Ensure that the init of one Singleton can itself init another singleton."""
    nested = nested_singleton()
    single = singleton_class()

    assert nested.single is single


def test_initializing_singleton_is_atomic(singleton_class):
    """
    Forces a race condition on initialization and ensures that only 1 instances is created

    This test is setting up the race condition by creating 2 threads, each which will ask for a reference
    to the target singleton. The __init__ method of that singleton can be controlled by and communicate with
    this test code via interaction with 2 Event objects. The first thread will be launched and block
    (via Event.wait) inside the __init__ of the Singleton. And then the 2nd thread will be unleashed and the
    test code can ensure that this second thread can't get into the __init__, because of the atomicity of
    the singleton.

    Some my content that doing this test by mocking out the Lock is better/simpler. This implementation uses
    real threads and *zero* knowledge of the internals of the Singleton implementation. Thus it is less fragile.
    Singleton can change implementation to use some other Locking scheme... and nothing here changes. A mock version
    would break in that eventuality.
    """
    results = []
    thread1_inside_singleton, thread1_is_released = Event(), Event()
    thread2_inside_singleton, thread2_has_started = Event(), Event()

    def entry(on_enter, block_on, thread_has_started):
        if thread_has_started:
            thread_has_started.set()
        single = singleton_class(on_enter, block_on)
        results.append(single)

    thread1 = Thread(target=entry, args=(thread1_inside_singleton, thread1_is_released, None))
    thread1.start()

    thread1_inside_singleton.wait()

    thread2 = Thread(target=entry, args=(thread2_inside_singleton, None, thread2_has_started))
    thread2.start()

    thread2_has_started.wait()              # We block until the thread is known to have started.
    assert not thread2_inside_singleton.wait(0.01)  # Wait a bit ensuring that the thread never makes it inside
    assert thread2.is_alive()               # And yet the thread is still alive.

    thread1_is_released.set()               # releasing thread1 will allow both threads to complete.

    thread1.join()
    thread2.join()
    assert not thread2_inside_singleton.wait(0)   # Re-ensure that thread2 never made it inside the singleton __init__
    assert results[0] is results[1]         # And of course there's only 1 instance of the singleton
