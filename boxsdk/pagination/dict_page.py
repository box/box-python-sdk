# coding: utf-8
from typing import Any

from .page import Page


class DictPage(Page):
    def __getitem__(self, key: str) -> Any:
        return self._response_object[self._item_entries_key_name][key]
