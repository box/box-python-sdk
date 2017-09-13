# coding: utf-8

from __future__ import absolute_import, unicode_literals

from functools import wraps
import json
from time import sleep

from bottle import template
import six

from test.functional.mock_box.util.http_utils import abort


try:
    import jsonpatch
except ValueError:
    # jsonpatch==1.14 on Python 3.6 cannot be imported.
    # It fails with the following stacktrace:
    #
    #       .tox/py/lib/python3.6/site-packages/jsonpatch.py:114: in <module>
    #           json.load = get_loadjson()
    #       .tox/py/lib/python3.6/site-packages/jsonpatch.py:108: in get_loadjson
    #           argspec = inspect.getargspec(json.load)
    #       lib/python3.6/inspect.py:1039: in getargspec
    #           raise ValueError("Function has keyword-only arguments or annotations"
    #       E   ValueError: Function has keyword-only arguments or annotations, use getfullargspec() API which can support them
    #
    # Until jsonpatch fixes this issue, we cannot use jsonpatch on Python >=3.6.
    jsonpatch = None


def allow_chaos(method):
    """Decorator for a method to allow erroneous operation."""
    method.call_number = 0
    added_chaos = []

    def add_chaos(chaos, should_apply=lambda call_number, *_: True):
        added_chaos.append((chaos, should_apply))

    def reset_chaos(call_number=0):
        del added_chaos[:]
        method.call_number = call_number

    @wraps(method)
    def chaotic_method(self, *args, **kwargs):
        skip_chaos = kwargs.pop('skip_chaos', False)
        method_to_apply = method
        if not skip_chaos:
            method.call_number += 1
            for chaos, should_apply in added_chaos:
                should_apply_result = False
                if isinstance(should_apply, int):
                    should_apply_result = method.call_number == should_apply
                elif hasattr(should_apply, '__iter__'):
                    should_apply_result = method.call_number in should_apply
                elif hasattr(should_apply, '__call__'):
                    should_apply_result = should_apply(method.call_number, args, kwargs)
                if should_apply_result:
                    method_to_apply = chaos(method_to_apply)
        return method_to_apply(self, *args, **kwargs)

    chaotic_method.add_chaos = add_chaos
    chaotic_method.reset_chaos = reset_chaos

    return chaotic_method


def delay(delay_seconds):
    return lambda delayed_function: lambda *args, **kwargs: sleep(delay_seconds) or delayed_function(*args, **kwargs)


def error(code, message=None, headers=None):
    return lambda erroneous_function: lambda *args, **kwargs: abort(code, message=message, headers=headers)


def html(method):
    return lambda *args, **kwargs: template('html_response', response=method(*args, **kwargs))


def xml(method):
    return lambda *args, **kwargs: template('xml_response', response=method(*args, **kwargs))


def patch(operations):
    if jsonpatch:
        json_patch = jsonpatch.JsonPatch(operations)

        def patcher(doc):
            return json_patch.apply(doc)

    else:

        def patcher(doc):
            # If jsonpatch could not be imported, then `@chaos_utils.patch()`
            # will be disabled, and will silently return values unmodified,
            # without applying the JSON patch operations.
            return doc

    def inner(patched_function):
        def patched_inner(*args, **kwargs):
            return_value = patched_function(*args, **kwargs)
            not_json = False
            if not isinstance(return_value, six.text_type):
                return_value = json.dumps(return_value)
                not_json = True
            return_value = patcher(return_value)
            if not_json:
                return_value = json.loads(return_value)
            return return_value
        return patched_inner
    return inner
