# coding: utf-8

from __future__ import absolute_import, unicode_literals


__doc__ = """pytest fixtures that can help with testing boxsdk-powered applications."""   # pylint:disable=redefined-builtin


pytest_plugins = ['boxsdk.pytest_plugin.betamax']   # pylint:disable=invalid-name
