# coding: utf-8

from __future__ import division, unicode_literals


from datetime import timedelta

if not hasattr(timedelta, 'total_seconds'):
    def total_seconds(delta):
        return (delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 10 ** 6) / 10 ** 6
else:
    def total_seconds(delta):
        return delta.total_seconds()
