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
        return self.__class__(self._session, self._object_id, box_response.json())

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
            developer API documentation <https://box-content.readme.io/docs/>.
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
        url = self.get_url()
        box_response = self._session.put(url, data=json.dumps(data), params=params, headers=headers, **kwargs)
        response = box_response.json()
        return self.__class__(
            session=self._session,
            object_id=self._object_id,
            response_object=response,
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
        """Equality as determined by object id"""
        return self._object_id == other.object_id

    def _paging_wrapper(self, url, starting_index, limit, factory=None):
        """
        Helper function that turns any paging API into a generator that transparently implements the paging for
        the caller.

        A caller wanting to implement their own paging can do so by managing the starting_index & limit params,
        and never iterating over more than 'limit' items per call. For example:

            first_ten = list(itertools.islice(_paging_wrapper(..., 0, 10, ...), 10))
            second_ten = list(itertools.islice(_paging_wrapper(..., 10, 10, ...), 10))
            third_ten = list(itertools.islice(_paging_wrapper(..., 20, 10, ...), 10))
            ...
        When one of the lists has less than 10 items... the end has been reached.

        Caveat: any hidden items (see the Box Developer API for more details) will render the above
        inaccurate. Hidden results will lead the above get_slice() code to trigger API calls at non-expected places.

        :param starting_index:
            The index at which to begin.
        :type starting_index:
            `int`
        :param limit:
            The maximum number of items to return in a page.
        :type limit:
            `int`
        :param factory:
            A callable factory method which creates the object instances. Signature should match the __init__
            signature of BaseObject. If no factory is given then the Translator factory is used.
        :type factory:
            `callable` or None
        :returns:
            A generator of 3-tuples. Each tuple contains:
            1) An instance returned by the given factory callable.
            2) The number of objects in the current page.
            3) Index the current instance in the current page.
        :rtype:
            `generator` of `tuple` of (varies, `int`, `int`)
        """
        current_index = starting_index

        while True:
            params = {'limit': limit, 'offset': current_index}
            box_response = self._session.get(url, params=params)
            response = box_response.json()

            current_page_size = len(response['entries'])
            for index_in_current_page, item in enumerate(response['entries']):
                instance_factory = factory
                if not instance_factory:
                    instance_factory = self.translator.translate(item['type'])
                instance = instance_factory(self._session, item['id'], item)
                yield instance, current_page_size, index_in_current_page

            current_index += limit
            if current_index >= response['total_count']:
                break

    def clone(self, session=None):
        """Base class override."""
        return self.__class__(
            session or self._session,
            self._object_id,
            self._response_object,
        )
