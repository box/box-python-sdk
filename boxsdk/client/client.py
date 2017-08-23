# coding: utf-8

from __future__ import unicode_literals, absolute_import
import json

from ..config import API
from ..session.box_session import BoxSession
from ..network.default_network import DefaultNetwork
from ..object.cloneable import Cloneable
from ..util.api_call_decorator import api_call
from ..object.search import Search
from ..object.events import Events
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection
from ..util.shared_link import get_shared_link_header


class Client(Cloneable):

    def __init__(
            self,
            oauth=None,
            network_layer=None,
            session=None,
    ):
        """
        :param oauth:
            OAuth2 object used by the session to authorize requests.
        :type oauth:
            :class:`OAuth2`
        :param network_layer:
            The Network layer to use. If none is provided then an instance of :class:`DefaultNetwork` will be used.
        :type network_layer:
            :class:`Network`
        :param session:
            The session object to use. If None is provided then an instance of :class:`BoxSession` will be used.
        :type session:
            :class:`BoxSession`
        """
        super(Client, self).__init__()
        self._oauth = oauth
        self._session = session or BoxSession(oauth=oauth, network_layer=(network_layer or DefaultNetwork()))

    @property
    def auth(self):
        """
        Get the :class:`OAuth2` instance the client is using for auth to Box.

        :rtype:
            :class:`OAuth2`
        """
        return self._oauth

    @property
    def session(self):
        """
        Get the :class:`BoxSession` instance the client is using.

        :rtype:
            :class:`BoxSession`
        """
        return self._session

    @property
    def translator(self):
        """The translator used for translating Box API JSON responses into `BaseAPIJSONObject` smart objects.

        :rtype:   :class:`Translator`
        """
        return self._session.translator

    def folder(self, folder_id):
        """
        Initialize a :class:`Folder` object, whose box id is folder_id.

        :param folder_id:
            The box id of the :class:`Folder` object. Can use '0' to get the root folder on Box.
        :type folder_id:
            `unicode`
        :return:
            A :class:`Folder` object with the given folder id.
        :rtype:
            :class:`Folder`
        """
        return self.translator.translate('folder')(session=self._session, object_id=folder_id)

    def file(self, file_id):
        """
        Initialize a :class:`File` object, whose box id is file_id.

        :param file_id:
            The box id of the :class:`File` object.
        :type file_id:
            `unicode`
        :return:
            A :class:`File` object with the given file id.
        :rtype:
            :class:`File`
        """
        return self.translator.translate('file')(session=self._session, object_id=file_id)

    def user(self, user_id='me'):
        """
        Initialize a :class:`User` object, whose box id is user_id.

        :param user_id:
            The user id of the :class:`User` object. Can use 'me' to get the User for the current/authenticated user.
        :type user_id:
            `unicode`
        :return:
            A :class:`User` object with the given id.
        :rtype:
            :class:`User`
        """
        return self.translator.translate('user')(session=self._session, object_id=user_id)

    def group(self, group_id):
        """
        Initialize a :class:`Group` object, whose box id is group_id.

        :param group_id:
            The box id of the :class:`Group` object.
        :type group_id:
            `unicode`
        :return:
            A :class:`Group` object with the given group id.
        :rtype:
            :class:`Group`
        """
        return self.translator.translate('group')(session=self._session, object_id=group_id)

    def collaboration(self, collab_id):
        """
        Initialize a :class:`Collaboration` object, whose box id is collab_id.

        :param collab_id:
            The box id of the :class:`Collaboration` object.
        :type collab_id:
            `unicode`
        :return:
            A :class:`Collaboration` object with the given group id.
        :rtype:
            :class:`Collaboration`
        """
        return self.translator.translate('collaboration')(session=self._session, object_id=collab_id)

    @api_call
    def users(self, limit=None, offset=0, filter_term=None):
        """
        Get a list of all users for the Enterprise along with their user_id, public_name, and login.

        :param limit:
            The maximum number of users to return. If not specified, the Box API will determine an appropriate limit.
        :type limit:
            `int` or None
        :param offset:
            The user index at which to start the response.
        :type offset:
            `int`
        :param filter_term:
            Filters the results to only users starting with the filter_term in either the name or the login.
        :type filter_term:
            `unicode` or None
        :return:
            The list of all users in the enterprise.
        :rtype:
            `list` of :class:`User`
        """
        url = '{0}/users'.format(API.BASE_API_URL)
        params = dict(offset=offset)
        if limit is not None:
            params['limit'] = limit
        if filter_term is not None:
            params['filter_term'] = filter_term
        box_response = self._session.get(url, params=params)
        response = box_response.json()
        user_class = self.translator.translate('user')
        return [user_class(
            session=self._session,
            object_id=item['id'],
            response_object=item,
        ) for item in response['entries']]

    @api_call
    def search(
            self,
            query,
            limit,
            offset,
            ancestor_folders=None,
            file_extensions=None,
            metadata_filters=None,
            result_type=None,
            content_types=None
    ):
        """
        Search Box for items matching the given query.

        :param query:
            The string to search for.
        :type query:
            `unicode`
        :param limit:
            The maximum number of items to return.
        :type limit:
            `int`
        :param offset:
            The search result at which to start the response.
        :type offset:
            `int`
        :param ancestor_folders:
            Folder ids to limit the search to.
        :type ancestor_folders:
            `iterable` of :class:`Folder`
        :param file_extensions:
            File extensions to limit the search to.
        :type file_extensions:
            `iterable` of `unicode`
        :param metadata_filters:
            Filters used for metadata search
        :type metadata_filters:
            :class:`MetadataSearchFilters`
        :param result_type:
            Which type of result you want. Can be file or folder.
        :type result_type:
            `unicode`
        :param content_types:
            Which content types to search. Valid types include name, description, file_content, comments, and tags.
        :type content_types:
            `Iterable` of `unicode`
        :return:
            A list of items that match the search query.
        :rtype:
            `list` of :class:`Item`
        """
        return Search(self._session).search(
            query=query,
            limit=limit,
            offset=offset,
            ancestor_folders=ancestor_folders,
            file_extensions=file_extensions,
            metadata_filters=metadata_filters,
            result_type=result_type,
            content_types=content_types,
        )

    def events(self):
        """
        Get an events object that can get the latest events from Box or set up a long polling event subscription.
        """
        return Events(self._session)

    def group_membership(self, group_membership_id):
        """
        Initialize a :class:`GroupMembership` object, whose box id is group_membership_id.

        :param group_membership_id:
            The box id of the :class:`GroupMembership` object.
        :type group_membership_id:
            `unicode`
        :return:
            A :class:`GroupMembership` object with the given membership id.
        :rtype:
            :class:`GroupMembership`
        """
        return self.translator.translate('group_membership')(
            session=self._session,
            object_id=group_membership_id,
        )

    @api_call
    def groups(self):
        """
        Get a list of all groups for the current user.

        :return:
            The list of all groups.
        :rtype:
            `list` of :class:`Group`
        """
        url = '{0}/groups'.format(API.BASE_API_URL)
        box_response = self._session.get(url)
        response = box_response.json()
        group_class = self.translator.translate('group')
        return [group_class(
            session=self._session,
            object_id=item['id'],
            response_object=item,
        ) for item in response['entries']]

    @api_call
    def create_group(self, name):
        """
        Create a group with the given name.

        :param name:
            The name of the group.
        :type name:
            `unicode`
        :return:
            The newly created Group.
        :rtype:
            :class:`Group`
        :raises:
            :class:`BoxAPIException` if current user doesn't have permissions to create a group.
        """
        url = '{0}/groups'.format(API.BASE_API_URL)
        body_attributes = {
            'name': name,
        }
        box_response = self._session.post(url, data=json.dumps(body_attributes))
        response = box_response.json()
        return self.translator.translate('group')(
            session=self._session,
            object_id=response['id'],
            response_object=response,
        )

    @api_call
    def get_recent_items(self, limit=None, marker=None, fields=None, **collection_kwargs):
        """
        Get the user's recently accessed items.

        :param: limit
            The maximum number of items to return. If limit is set to None, then the default
            limit (returned by Box in the response) is used. See https://developer.box.com/reference#get-recent-items
            for default.
        :type: limit
            `int` or None
        :param marker:
            The index at which to start returning items.
        :type marker:
            `str` or None
        :param fields:
            List of fields to request on the file or folder which the `RecentItem` references.
        :type fields:
            `Iterable` of `unicode`
        :param **collection_kwargs:
            Keyword arguments passed to `MarkerBasedObjectCollection`.
        :type **collection_args:
            `dict`
        :returns:
            An iterator on the user's recent items
        :rtype:
            :class:`MarkerBasedObjectCollection`
        """
        return MarkerBasedObjectCollection(
            self.session,
            self.get_url('recent_items'),
            limit=limit,
            fields=fields,
            marker=marker,
            **collection_kwargs
        )

    @api_call
    def get_shared_item(self, shared_link, password=None):
        """
        Get information about a Box shared link. https://box-content.readme.io/reference#get-a-shared-item

        :param shared_link:
            The shared link.
        :type shared_link:
            `unicode`
        :param password:
            The password for the shared link.
        :type password:
            `unicode`
        :return:
            The item referred to by the shared link.
        :rtype:
            :class:`Item`
        :raises:
            :class:`BoxAPIException` if current user doesn't have permissions to view the shared link.
        """
        response = self.make_request(
            'GET',
            '{0}/shared_items'.format(API.BASE_API_URL),
            headers=get_shared_link_header(shared_link, password),
        ).json()
        return self.translator.translate(response['type'])(
            session=self._session.with_shared_link(shared_link, password),
            object_id=response['id'],
            response_object=response,
        )

    @api_call
    def make_request(self, method, url, **kwargs):
        """
        Make an authenticated request to the Box API.

        :param method:
            The HTTP verb to use for the request.
        :type method:
            `unicode`
        :param url:
            The URL for the request.
        :type url:
            `unicode`
        :return:
            The network response for the given request.
        :rtype:
            :class:`BoxResponse`
        :raises:
            :class:`BoxAPIException`
        """
        return self._session.request(method, url, **kwargs)

    @api_call
    def create_user(self, name, login=None, **user_attributes):
        """
        Create a new user. Can only be used if the current user is an enterprise admin, or the current authorization
        scope is a Box developer edition instance.

        :param name:
            The user's display name.
        :type name:
            `unicode`
        :param login:
            The user's email address. Required for an enterprise user, but None for an app user.
        :type login:
            `unicode` or None
        :param user_attributes:
            Additional attributes for the user. See the documentation at
            https://box-content.readme.io/#create-an-enterprise-user for enterprise users
            or https://box-content.readme.io/docs/app-users for app users.
        """
        url = '{0}/users'.format(API.BASE_API_URL)
        user_attributes['name'] = name
        if login is not None:
            user_attributes['login'] = login
        else:
            user_attributes['is_platform_access_only'] = True
        box_response = self._session.post(url, data=json.dumps(user_attributes))
        response = box_response.json()
        return self.translator.translate('user')(
            session=self._session,
            object_id=response['id'],
            response_object=response,
        )

    def clone(self, session=None):
        """Base class override."""
        return self.__class__(oauth=self._oauth, session=(session or self._session))

    def get_url(self, endpoint, *args):
        """
        Return the URL for the given Box API endpoint.

        :param endpoint:
            The name of the endpoint.
        :type endpoint:
            `url`
        :param args:
            Additional parts of the endpoint URL.
        :type args:
            `Iterable`
        :rtype:
            `unicode`
        """
        # pylint:disable=no-self-use
        return self._session.get_url(endpoint, *args)
