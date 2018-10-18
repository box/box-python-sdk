# coding:utf-8
from __future__ import unicode_literals, absolute_import
from .base_object import BaseObject


class LegalHold(BaseObject):

    """Represents the legal hold policy for a file version"""
    _item_type = 'legal_hold'

    def get_url(self, *args):
        return self._session.get_url('file_version_legal_holds', self._object_id, *args)
