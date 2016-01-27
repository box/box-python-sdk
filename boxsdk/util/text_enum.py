# coding: utf-8

from __future__ import absolute_import, unicode_literals
from enum import Enum
from six import text_type


class TextEnum(text_type, Enum):
    def __repr__(self):
        return self._value_  # pylint:disable=no-member

    def __str__(self):
        return str(self.value)  # pylint:disable=no-member
