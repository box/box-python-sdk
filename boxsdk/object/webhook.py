# coding: utf-8

import base64
import hashlib
import hmac
from typing import Optional

from .base_object import BaseObject


class Webhook(BaseObject):
    """Represents a Box Webhook."""

    _item_type = 'webhook'

    @staticmethod
    def validate_message(
            body: bytes,
            headers: dict,
            primary_signature_key: str,
            secondary_signature_key: str = None
    ) -> bool:
        """
        Validates a `Webhook` message.

        :param body:
            The encoded webhook body.
        :param headers:
            The headers for the `Webhook` notification.
        :param primary_signature_key:
            The `Webhook` primary signature key for this application.
        :param secondary_signature_key:
            The `Webhook` secondary signature key for this application.
        :return:
            A `bool` indicating whether a webhook message was validated or not
        """

        primary_signature = _compute_signature(body, headers, primary_signature_key)
        if primary_signature is not None and hmac.compare_digest(primary_signature, headers.get('box-signature-primary')):
            return True

        if secondary_signature_key:
            secondary_signature = _compute_signature(body, headers, secondary_signature_key)
            if secondary_signature is not None and hmac.compare_digest(secondary_signature, headers.get('box-signature-secondary')):
                return True
            return False

        return False


def _compute_signature(body: bytes, headers: dict, signature_key: str) -> Optional[str]:
    """
    Computes the Hmac for the webhook notification given one signature key.

    :param body:
        The encoded webhook body.
    :param headers:
        The headers for the `Webhook` notification.
    :param signature_key:
        The `Webhook` signature key for this application.
    :return:
        An Hmac signature.
    """
    if signature_key is None:
        return None
    if headers.get('box-signature-version') != '1':
        return None
    if headers.get('box-signature-algorithm') != 'HmacSHA256':
        return None

    encoded_signature_key = signature_key.encode('utf-8')
    encoded_delivery_time_stamp = headers.get('box-delivery-timestamp').encode('utf-8')
    new_hmac = hmac.new(encoded_signature_key, digestmod=hashlib.sha256)
    new_hmac.update(body + encoded_delivery_time_stamp)
    signature = base64.b64encode(new_hmac.digest()).decode()
    return signature
