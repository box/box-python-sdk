# coding: utf-8

from __future__ import unicode_literals
import json
from .base_object import BaseObject
from boxsdk.config import API
from boxsdk.util.translator import Translator
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection


def _compute_signature(body, headers, signature_key):
    if signature_key is None:
        return None
# convert to braces
    if headers.box-signature-version != '1':
        return None

    if headers.box-signature-algorithm != '1':
        return None

    new_hmac = hmac.new('sha256', signature_key)
    new_hmac.update(body)
    new_hmac.update(headers.box-delivery-timestamp)

    signature = new_hmac.digest

    return signature

class Webhook(BaseObject):
    """Represents a Box task."""

    _item_type = 'webhook'
# secondary signature key is optional 
    @staticmethod
    def validate_message(body, headers, primary_signature_key, secondary_signature_key):

        primary_signature = _compute_signature(body, headers, primary_signature_key)

        if primary_signature and primary_signature_key == headers.box_secondary_signature_key:
            return True

        secondary_signature = _compute_signature(body, headers, secondary_signature_key)

        if secondary_signature and secondary_signature_key == headers.box-signature-secondary:
            return True

        return False
