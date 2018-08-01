# coding: utf-8

from __future__ import unicode_literals

import base64
import hashlib
import hmac
import json

from .base_object import BaseObject


def _compute_signature(body, headers, signature_key):
    """
    Computes the Hmac for the webhook notification given one signature key.

    :param body:
        The encoded webhook body.
    :type:
        `bytes`
    :param headers:
        The headers for the `Webhook` notification.
    :type headers:
        `dict`
    :param signature_key:
        The `Webhook` signature key for this application.
    :type signature_key:
        `unicode`
    """
    if signature_key is None:
        return None

    if headers.get('box-signature-version') != '1':
        return None

    if headers.get('box-signature-algorithm') != 'HmacSHA256':
        return None
    print('Signature Key: ' + signature_key)
    encoded_signature_key = signature_key.encode()
    encoded_delivery_time_stamp = headers.get('box-delivery-timestamp').encode()

    new_hmac = hmac.new(encoded_signature_key, digestmod=hashlib.sha256)
    new_hmac.update(body)
    new_hmac.update(encoded_delivery_time_stamp)

    signature = base64.b64encode(new_hmac.digest()).decode()
    print('Signature: ' + signature)
    return signature


class Webhook(BaseObject):
    """Represents a Box task."""

    _item_type = 'webhook'

    @staticmethod
    def validate_message(body, headers, primary_signature_key, secondary_signature_key=None):
        """
        Validates a `Webhook` message.

        :param body:
            The encoded webhook body.
        :type:
            `bytes`
        :param headers:
            The headers for the `Webhook` notification.
        :type headers:
            `dict`
        :param primary_signature_key:
            The `Webhook` primary signature key for this application.
        :type primary_signature_key:
            `unicode`
        :param secondary_signature_key:
            The `Webhook` secondary signature key for this application.
        :type secondary_signature_key:
            `unicode`
        """
        if isinstance(body, dict):
            body = json.dumps(body, separators=(',', ':')).encode()

        primary_signature = _compute_signature(body, headers, primary_signature_key)
        print('Primary Signature: ' + primary_signature)
        if primary_signature and primary_signature == headers.get('box-signature-primary'):
            return True

        if secondary_signature_key:
            secondary_signature = _compute_signature(body, headers, secondary_signature_key)
            print('Secondary Signature: ' + secondary_signature)
            if secondary_signature and secondary_signature == headers.get('box-signature-secondary'):
                return True
            return False

        return False
