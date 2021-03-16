# coding: utf-8

from __future__ import unicode_literals, absolute_import
import json

from .base_endpoint import BaseEndpoint
from .base_api_json_object import BaseAPIJSONObject
from ..util.api_call_decorator import api_call


class BaseObject(BaseEndpoint, BaseAPIJSONObject):
    """A Box API endpoint for interacting with a Box object."""

    def __init__(self, session, object_id, response_object=None):
        """
        :param session:
            The Box session used to make requests.
        :type session:
            :class:`BoxSession`
        :param object_id:
            The Box ID for the object.
        :type object_id:
            `unicode`
        :param response_object:
            A JSON object representing the object returned from a Box API request.
        :type response_object:
            `dict`
        """
        super(BaseObject, self).__init__(session=session, response_object=response_object)
        self._object_id = object_id

    @property
    def _description(self):
        """Base class override.  Return a description for the object."""
        if 'name' in self._response_object:
            return '{0} ({1})'.format(self._object_id, self.name)  # pylint:disable=no-member
        return '{0}'.format(self._object_id)

    def get_url(self, *args):
        """
        Base class override.
        Return the given object's URL, appending any optional parts as specified by args.
        """
        # pylint:disable=arguments-differ
        return super(BaseObject, self).get_url('{0}s'.format(self._item_type), self._object_id, *args)

    def get_type_url(self):
        """
        Return the URL for type of the given resource.

        :rtype:
            `unicode`
        """
        return super(BaseObject, self).get_url('{0}s'.format(self._item_type))

    @property
    def object_id(self):
        """Return the Box ID for the object.

        :rtype:
            `unicode`
        """
        return self._object_id

    @api_call
    def get(self, fields=None, headers=None):
        """
        Get information about the object, specified by fields. If fields is None, return the default fields.

        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :param headers:
            Additional headers to send with the request.
        :type headers:
            `dict`
        :return:
            An object of the same type that has the requested information.
        :rtype:
            :class:`BaseObject`
        """
        url = self.get_url()
        params = {'fields': ','.join(fields)} if fields else None
        box_response = self._session.get(url, params=params, headers=headers)
        return self.translator.translate(
            session=self._session,
            response_object=box_response.json(),
        )

    @api_call
    def update_info(self, data, params=None, headers=None, **kwargs):
        """Update information about this object.

        Send a PUT to the object's base endpoint to modify the provided
        attributes.

        :param data:
            The updated information about this object.
            Must be JSON serializable.
            Update the object attributes in data.keys(). The semantics of the
            values depends on the the type and attributes of the object being
            updated. For details on particular semantics, refer to the Box
            developer API documentation <https://developer.box.com/>.
        :type data:
            `dict`
        :param params:
            (optional) Query string parameters for the request.
        :type params:
            `dict` or None
        :param headers:
            (optional) Extra HTTP headers for the request.
        :type headers:
            `dict` or None
        :param kwargs:
            Optional arguments that ``put`` takes.
        :return:
            The updated object.
            Return a new object of the same type, without modifying the
            original object passed as self.
            Construct the new object with all the default attributes that are
            returned from the endpoint.
        :rtype:
            :class:`BaseObject`
        """
        # pylint:disable=no-else-return
        url = self.get_url()
        box_response = self._session.put(url, data=json.dumps(data), params=params, headers=headers, **kwargs)
        if 'expect_json_response' in kwargs and not kwargs['expect_json_response']:
            return box_response.ok
        else:
            return self.translator.translate(
                session=self._session,
                response_object=box_response.json(),
            )

    @api_call
    def delete(self, params=None, headers=None):
        """ Delete the object.

        :param params:
            Additional parameters to send with the request. Can be None
        :type params:
            `dict` or None
        :param headers:
            Any customer headers to send with the request. Can be None
        :type headers:
            `dict` or None
        :returns:
            Whether or not the delete was successful.
        :rtype:
            `bool`
        :raises:
            :class:`BoxAPIException` in case of unexpected errors.
        """
        url = self.get_url()
        # ??? There's a question about why params forces a default to {}, while headers doesn't. Looking for
        # confirmation that the below is correct.
        box_response = self._session.delete(url, expect_json_response=False, params=params or {}, headers=headers)
        return box_response.ok

    def __eq__(self, other):
        """Equality as determined by object id and type"""
        if isinstance(other, BaseObject):
            # Two objects are considered the same if they have the same address in the API
            return self.get_url() == other.get_url()

        return NotImplemented

    def __ne__(self, other):
        """Equality as determined by object id and type"""
        return not self == other

    def __hash__(self):
        return hash((self._object_id, self._item_type))

    def clone(self, session=None):
        """Base class override."""
        return self.__class__(
            session or self._session,
            self._object_id,
            self._response_object,
        )
