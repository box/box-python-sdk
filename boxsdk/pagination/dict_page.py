# coding: utf-8

from .page import Page


class DictPage(Page):
    def __getitem__(self, key):
        item_json = self._response_object[self._item_entries_key_name][key]

        return item_json
