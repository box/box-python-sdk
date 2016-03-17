# coding: utf-8

from __future__ import unicode_literals
from abc import ABCMeta
import json

import six

from boxsdk.object.base_endpoint import BaseEndpoint
from boxsdk.util.translator import Translator


class ObjectMeta(ABCMeta):
    """
    Metaclass for Box API objects. Registers classes so that API responses can be translated to the correct type.
    Relies on the _item_type field defined on the classes to match the type property of the response json.
    But the type-class mapping will only be registered if the module of the class is imported.
    So it's also important to add the module name to __all__ in object/__init__.py.
    """
    def __init__(cls, name, bases, attrs):
        super(ObjectMeta, cls).__init__(name, bases, attrs)
        item_type = attrs.get('_item_type', None)
        if item_type is not None:
            Translator().register(item_type, cls)


@six.add_metaclass(ObjectMeta)
class BaseObject(BaseEndpoint):
    """
    A Box API endpoint for interacting with a Box object.
    """
    _item_type = None

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
            The Box API response representing the object.
        :type response_object:
            :class:`BoxResponse`
        """
        super(BaseObject, self).__init__(session)
        self._object_id = object_id
        self._response_object = response_object or {}
        self.__dict__.update(self._response_object)

    def __getitem__(self, item):
        """Base class override. Try to get the attribute from the API response object."""
        return self._response_object[item]

    def __repr__(self):
        """Base class override. Return a human-readable representation using the Box ID or name of the object."""
        description = '<Box {0} - {1}>'.format(self.__class__.__name__, self._description)
        if six.PY2:
            return description.encode('utf-8')
        else:
            return description

    @property
    def _description(self):
        if 'name' in self._response_object:
            return '{0} ({1})'.format(self._object_id, self.name)  # pylint:disable=no-member
        else:
            return '{0}'.format(self._object_id)

    def get_url(self, *args):
        """
        Base class override.
        Return the given object's URL, appending any optional parts as specified by args.
        """
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
        """Base class override. Equality is determined by object id."""
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
                    instance_factory = Translator().translate(item['type'])
                instance = instance_factory(self._session, item['id'], item)
                yield instance, current_page_size, index_in_current_page

            current_index += limit
            if current_index >= response['total_count']:
                break

    def as_user(self, user):
        """ Base class override. """
        return self.__class__(self._session.as_user(user), self._object_id, self._response_object)

    def with_shared_link(self, shared_link, shared_link_password):
        """ Base class override. """
        return self.__class__(
            self._session.with_shared_link(shared_link, shared_link_password),
            self._object_id,
            self._response_object,
        )
