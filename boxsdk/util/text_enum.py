# coding: utf-8

from enum import Enum


class TextEnum(str, Enum):
    def __repr__(self):
        return self._value_  # pylint:disable=no-member

    def __str__(self):
        return str(self.value)  # pylint:disable=no-member
