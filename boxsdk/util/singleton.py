# coding: utf-8

from __future__ import unicode_literals
from threading import RLock


class Singleton(type):
    """
    Metaclass for implementing the singleton pattern.

    Sample usage:
        @add_metaclass(Singleton)
        class my_singleton(object):
            def __init__(self):
                pass
    """
    _instances = {}
    _lock = RLock()

    def __call__(cls, *args, **kwargs):
        """
        When the class is instantiated, return the singleton if it exists; else create it and store for the next use.
        """
        if cls not in Singleton._instances:
            # Using an RLock, in case the singleton being initialized itself initializes another singleton.
            # RLock's are slow... but the 'if' just above ensures that slowness is only suffered when any
            # Singleton subclass is first initialized. After that the outer 'if' above will skip this code.
            with Singleton._lock:
                if cls not in Singleton._instances:
                    Singleton._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return Singleton._instances[cls]
