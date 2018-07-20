# coding: utf-8

from __future__ import unicode_literals

from .base_object import BaseObject

class DevicePin(BaseObject):
    """Represents the device pinner"""


    def get_url(self, *args):
        return self._session.get_url('device_pinners', self._object_id, *args)

    _item_type = 'device_pinner'
