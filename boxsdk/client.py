# coding: utf-8

from __future__ import unicode_literals
import json

from .config import API
from .session.box_session import BoxSession
from .network.default_network import DefaultNetwork
from .object.user import User
from .object.folder import Folder
from .object.search import Search
from .object.events import Events
from .object.file import File
from .object.group import Group
from .object.group_membership import GroupMembership


class Client(object):

    def __init__(self, oauth, network_layer=None):
        """
        :param oauth:
            OAuth2 object used by the session to authorize requests.
        :type oauth:
            :class:`OAuth2`
        :param network_layer:
            The Network layer to use. If none is provided then an instance of :class:`DefaultNetwork` will be used.
        :type network_layer:
            :class:`Network`
        """
        network_layer = network_layer or DefaultNetwork()
        self._session = BoxSession(oauth=oauth, network_layer=network_layer)

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
        return Folder(session=self._session, object_id=folder_id)

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
        return File(session=self._session, object_id=file_id)

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
        return User(session=self._session, object_id=user_id)

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
        return Group(session=self._session, object_id=group_id)

    def users(self):
        """
        Get a list of all users for the Enterprise along with their user_id, public_name, and login.

        :return:
            The list of all users in the enterprise.
        :rtype:
            `list` of :class:`User`
        """
        url = '{0}/users'.format(API.BASE_API_URL)
        box_response = self._session.get(url)
        response = box_response.json()
        return [User(self._session, item['id'], item) for item in response['entries']]

    def search(self, query, limit, offset, ancestor_folders=None, file_extensions=None):
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
            `list` of `unicode`
        :param file_extensions:
            File extensions to limit the search to.
        :type file_extensions:
            `list` of `unicode`
        :return:
            A list of items that match the search query.
        :rtype:
            `list` of :class:`Item`
        """
        return Search(self._session).search(query, limit, offset, ancestor_folders, file_extensions)

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
        return GroupMembership(session=self._session, object_id=group_membership_id)

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
        return [Group(self._session, item['id'], item) for item in response['entries']]

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
        return Group(self._session, response['id'], response)

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
