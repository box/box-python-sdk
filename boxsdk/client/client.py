# coding: utf-8

from __future__ import unicode_literals, absolute_import
import json

from ..config import API
from ..session.box_session import BoxSession
from ..network.default_network import DefaultNetwork
from ..object.user import User
from ..object.folder import Folder
from ..object.search import Search
from ..object.events import Events
from ..object.file import File
from ..object.group import Group
from ..object.webhook import Webhook
from ..object.group_membership import GroupMembership
from ..object.retention_policy import RetentionPolicy
from ..object.retention_policy_assignment import RetentionPolicyAssignment
from ..object.storage_policy import StoragePolicy
from ..object.storage_policy_assignment import StoragePolicyAssignment
from ..object.web_link import WebLink
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection
from ..pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection
from ..util.shared_link import get_shared_link_header
from ..util.translator import Translator
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection


class Client(object):

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
        network_layer = network_layer or DefaultNetwork()
        self._oauth = oauth
        self._network = network_layer
        self._session = session or BoxSession(oauth=oauth, network_layer=network_layer)

    @property
    def auth(self):
        """
        Get the :class:`OAuth2` instance the client is using for auth to Box.

        :rtype:
            :class:`OAuth2`
        """
        return self._oauth

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

    def comment(self, comment_id):
        """
        Initialize a :class:`Comment` object, whose Box ID is comment_id.

        :param comment_id:
            The Box ID of the :class:`Comment` object.
        :type comment_id:
            `unicode`
        :return:
            A :class:`Comment` object with the given comment ID.
        :rtype:
            :class:`Comment`
        """
        return Translator().translate('comment')(session=self._session, object_id=comment_id)

    def web_link(self, web_link_id):
        """
        Initialize a :class: `WebLink` object, whose box id is web_link_id.

        :param web_link_id:
            The box ID of the :class:`WebLink` object.
        :type web_link_id:
            `unicode`
        :return:
            A :class: `WebLink` object with the given entry ID.
        :rtype:
            :class:`WebLink`
        """
        return WebLink(session=self._session, object_id=web_link_id)

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

    def collection(self, collection_id):
        """
        Initialize a :class:`Collection` object, whose box ID is collection_id.

        :param collection_id:
            The box id of the :class:`Collection` object.
        :type collection_id:
            `unicode`
        :return:
            A :class:`Collection` object with the given collection ID.
        :rtype:
            :class:`Collection`
        """
        return Translator().translate('collection')(session=self._session, object_id=collection_id)

    def collections(self, limit=None, offset=0, fields=None):
        """
        Get a list of collections for the current user.

        :param limit:
            The maximum number of users to return. If not specified, the Box API will determine an appropriate limit.
        :type limit:
            `int` or None
        :param offset:
            The user index at which to start the response.
        :type offset:
            `int`
        """
        return LimitOffsetBasedObjectCollection(
            self._session,
            self._session.get_url('collections'),
            limit=limit,
            fields=fields,
            offset=offset,
            return_full_pages=False,
        )

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
        return [User(self._session, item['id'], item) for item in response['entries']]

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
        return Translator().translate(response['type'])(
            self._session.with_shared_link(shared_link, password),
            response['id'],
            response,
        )

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
        return User(self._session, response['id'], response)

    def as_user(self, user):
        """
        Returns a new client object with default headers set up to make requests as the specified user.

        :param user:
            The user to impersonate when making API requests.
        :type user:
            :class:`User`
        """
        return self.__class__(self._oauth, self._network, self._session.as_user(user))

    def with_shared_link(self, shared_link, shared_link_password):
        """
        Returns a new client object with default headers set up to make requests using the shared link for auth.

        :param shared_link:
            The shared link.
        :type shared_link:
            `unicode`
        :param shared_link_password:
            The password for the shared link.
        :type shared_link_password:
            `unicode`
        """
        return self.__class__(
            self._oauth,
            self._network,
            self._session.with_shared_link(shared_link, shared_link_password),
        )

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

    def webhook(self, webhook_id):
        """
        Initialize a :class: `Webhook` object, whose box id is webhook_id.
        :param webhook_id:
            The box ID of the :class: `Webhook` object.
        :type webhook_id:
            `unicode`
        :return:
            A :class: `Webhook` object with the given entry ID.
        :rtype:
            :class:`Webhook`
        """
        return Webhook(session-self._session, object_id=webhook_id)

    def create_webhook(self, target_id, target_type, triggers, address):
        """
        Create a webhook on the given file.

        :param triggers:
            Event types that trigger notifications for the target.
        :type triggers:
            `list of str`
        :param address:
            The url to send the notification to.
        :type address:
            `str`
        :return:
            A :class: `Webhook` object with the given entry ID.
        :rtype:
            :class:`Webhook`
        """
        url = '{0}/webhooks'.format(API.BASE_API_URL)
        webhook_attributes = {
            'target': {
                'type': target_type,
                'id': target_id,
            },
            'triggers': triggers,
            'address': address,
        }
        box_response = self._session.post(url, data=json.dumps(webhook_attributes))
        response = box_response.json()
        return Webhook(self._session, response['id'], response)

    def webhooks(self, marker=None, limit=None):
        """
        Get all webhooks in an enterprise.

        :param marker:
            The position marker at which to begin the response.
        :type marker:
            `str` or None
        :param limit:
            The maximum number of entries to return.
        :type limit:
            `int`
        :returns:
            An iterator of the entries in the webhook
        :rtype:
            :class:`BoxObjectCollection`
        """
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self.get_url('webhooks'),
            limit=limit,
            marker=marker,
        )

    def storage_policy(self, policy_id):
        """
        Initialize a :class:`StoragePolicy` object, whose box id is policy_id.

        :param policy_id:
            The box ID of the :class:`StoragePolicy` object.
        :type policy_id:
            `unicode`
        :return:
            A :class:`StoragePolicy` object with the given entry ID.
        :rtype:
            :class:`StoragePolicy`
        """
        return StoragePolicy(session=self._session, object_id=policy_id)

    def storage_policy_assignment(self, assignment_id):
        """
        Initialize a :class:`StoragePolicyAssignment` object, whose box id is assignment_id.

        :param assignment_id:
            The box ID of the :class:`StoragePolicyAssignment` object.
        :type assignment_id:
            `unicode`
        :return:
            A :class:`StoragePolicyAssignment` object with the given entry ID.
        :rtype:
            :class:`StoragePolicyAssignment`
        """
        return StoragePolicyAssignment(session=self._session, object_id=assignment_id)

    def storage_policies(self, limit=None, marker=None, fields=None):
        """
        Get the entries in the storage policy using limit-offset paging.

        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param marker:
            The paging marker to start paging from.
        :type marker:
            `str` or None
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries in the storage policy
        :rtype:
            :class:`BoxObjectCollection`
        """
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self.get_url('storage_policies'),
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )

    def storage_policy_assignments(self, resolved_for_type, resolved_for_id, marker=None, fields=None):
        """
        Get the entries in the storage policy assignment using limit-offset paging.

        :param resolved_for_type:
            Set to either `user` or `enterprise`
        :type limit:
            unicode
        :param resolved_for_id:
            The id of the user or enterprise
        :type limit:
            unicode
        :param marker:
            The paging marker to start paging from.
        :type marker:
            `str` or None
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries in the storage policy assignment
        :rtype:
            :class:`BoxObjectCollection`
        """
        additional_params = {
            'resolved_for_type': resolved_for_type,
            'resolved_for_id': resolved_for_id,
        }
        return MarkerBasedObjectCollection(
            session=self._session,
            url='{0}/storage_policy_assignments'.format(API.BASE_API_URL),
            additional_params=additional_params,
            limit=100,
            marker=marker,
            fields=fields,
        )

    def retention_policy(self, retention_id):
        """
        Initialize a :class:`RetentionPolicy` object, whose box id is retention_id.

        :param retention_id:
            The box ID of the :class:`RetentionPolicy` object.
        :type retention_id:
            `unicode`
        :return:
            A :class:`RetentionPolicy` object with the given entry ID.
        :rtype:
            :class:`RetentionPolicy`
        """
        return RetentionPolicy(session=self._session, object_id=retention_id)

    def retention_policy_assignment(self, assignment_id):
        """
        Initialize a :class:`RetentionPolicyAssignment` object, whose box id is assignment_id.

        :param assignment_id:
            The box ID of the :class:`RetentionPolicyAssignment` object.
        :type assignment_id:
            `unicode`
        :return:
            A :class:`RetentionPolicyAssignment` object with the given assignment ID.
        :rtype:
            :class:`RetentionPolicyAssignment`
        """
        return RetentionPolicyAssignment(session=self._session, object_id=assignment_id)

    def create_retention_policy(
            self,
            policy_name,
            policy_type,
            disposition_action,
            can_owner_extend_retention=False,
            are_owners_notified=False,
            retention_length=None,
            custom_notification_recipients=None,
    ):
        """
        Create a retention policy for the given enterprise.

        :param policy_name:
            The name of the retention policy.
        :type policy_name:
            `unicode`
        :param policy_type:
            Set to either `finite` or `indefinite`
        :type policy_type:
            `unicode`
        :param disposition_action:
            For `finite` policy can be set to `permanently delete` or `remove retention`.
            For `indefinite` policy this must be set to `remove_retention`
        :type disposition_action:
            `unicode`
        :param can_owner_extend_retention:
            The owner of a file will be allowed to extend the retention if set to true.
        :type can_owner_extend_retention:
            `boolean` or None
        :param are_owners_notified:
            The owner or co-owner will get notified when a file is nearing expiration.
        :type are_owners_notified:
            `boolean` or None
        :param retention_length:
            The amount of time in days to apply the retention policy to the selected content.
            Do not specify for `indefinite` policies, only for `finite` policies.
        :type are_owners_notified:
            `int` or None
        :param custom_notification_recipients:
            A custom list of user mini objects that should be notified when a file is nearing expiration.
        :type custom_notification_recipients:
            `list` or `User` objects
        :return:
            The newly created Retention Policy
        :rtype:
            :class:`RetentionPolicy`
        """
        url = '{0}/retention_policies'.format(API.BASE_API_URL)
        retention_attributes = {
            'policy_name': policy_name,
            'policy_type': policy_type,
            'disposition_action': disposition_action,
        }
        if can_owner_extend_retention is not None:
            retention_attributes['can_owner_extend_retention'] = can_owner_extend_retention
        if are_owners_notified is not None:
            retention_attributes['are_owners_notified'] = are_owners_notified
        if retention_length is not None:
            retention_attributes['retention_length'] = retention_length
        if custom_notification_recipients is not None:
            retention_attributes['custom_notification_recipients'] = custom_notification_recipients
        box_response = self._session.post(url, data=json.dumps(retention_attributes))
        response = box_response.json()
        return RetentionPolicy(self._session, response['id'], response)

    def retention_policies(
            self,
            policy_name=None,
            policy_type=None,
            created_by_user_id=None,
            limit=None,
            marker=None,
            fields=None,
    ):
        """
        Get the entries in the retention policy using marker-based paging.

        :param policy_name:
            The name of the retention policy.
        :type policy_name:
            `unicode` or None
        :param policy_type:
            Set to either `finite` or `indefinite`
        :type policy_type:
            `unicode` or None
        :param created_by_user_id:
            A user id to filter the retention policies.
        :type created_by_user_id:
            `unicode` or None
        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :type limit:
            `str` or None
        :param marker:
            The paging marker to start paging from
        :type marker:
            `str` or None
        :param fields:
            List of fields to request
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries in the retention policy
        """
        additional_params = {
            'policy_name': policy_name,
            'policy_type': policy_type,
            'created_by_user_id': created_by_user_id,
        }
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self._session.get_url('retention_policies'),
            additional_params=additional_params,
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )
