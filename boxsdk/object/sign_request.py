# coding: utf-8
from __future__ import unicode_literals, absolute_import

from .base_object import BaseObject
from ..util.api_call_decorator import api_call


class SignRequest(BaseObject):
    """
    Represents a Sign Request used by Box Sign
    Sign Requests are used to request e-signatures on documents from signers.
    A Sign Request can refer to one or more Box Files and can be sent to one or more Box Sign Request Signers.
    """
    _item_type = 'sign-request'

    def get_url(self, *args):
        """
        Returns the url for this sign request.
        """
        return self._session.get_url('sign_requests', self._object_id, *args)

    @api_call
    def cancel(self):
        """
        Cancels a sign request if it has not yet been signed or declined.
        Any outstanding signers will no longer be able to sign the document.

        :returns:
            The cancelled SignRequest object.
        :rtype:
            :class:`SignRequest`
        """
        url = self.get_url('cancel')
        response = self._session.post(url).json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def resend(self):
        """
        Attempts to resend a Sign Request to all signers that have not signed yet.
        There is a 10 minute cooling-off period between each resend request.

        :returns:
            HTTP status code
        :rtype:
            `int`
        """
        url = self.get_url('resend')
        response = self._session.post(url)
        return response
