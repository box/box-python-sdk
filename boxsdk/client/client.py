# coding: utf-8
# pylint: disable=too-many-lines
from __future__ import unicode_literals, absolute_import
import json

from ..auth.oauth2 import TokenResponse
from ..session.session import Session, AuthorizedSession
from ..object.cloneable import Cloneable
from ..util.api_call_decorator import api_call
from ..object.search import Search
from ..object.events import Events
from ..object.collaboration_whitelist import CollaborationWhitelist
from ..object.trash import Trash
from ..pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection
from ..util.shared_link import get_shared_link_header


class Client(Cloneable):
    unauthorized_session_class = Session
    authorized_session_class = AuthorizedSession

    def __init__(
            self,
            oauth,
            session=None,
    ):
        """
        :param oauth:
            OAuth2 object used by the session to authorize requests.
        :type oauth:
            :class:`OAuth2`
        :param session:
            The session object to use. If None is provided then an instance of :class:`AuthorizedSession` will be used.
        :type session:
            :class:`BoxSession`
        """
        super(Client, self).__init__()
        self._oauth = oauth
        if session is not None:
            self._session = session
        else:
            session = session or self.unauthorized_session_class()
            self._session = self.authorized_session_class(self._oauth, **session.get_constructor_kwargs())

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
        return self.translator.get('folder')(session=self._session, object_id=folder_id)

    def root_folder(self):
        """
        Returns a user's root folder object.
        """
        return self.folder('0')

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
        return self.translator.get('file')(session=self._session, object_id=file_id)

    def file_version(self, version_id):
        """
        Initialize a :class:`FileVersion` object, whose box id is version_id.

        :param version_id:
            The box id of the :class:`FileVersion` object.
        :type version_id:
            `unicode`
        :return:
            A :class:`FileVersion` object with the given file version id.
        :rtype:
            :class:`FileVersion`
        """
        return self.translator.get('file_version')(session=self._session, object_id=version_id)

    def upload_session(self, session_id):
        """
        Initialize a :class:`UploadSession` object, whose box id is session_id.

        :param session_id:
            The box id of the :class:`UploadSession` object.
        :type session_id:
            `unicode`
        :return:
            A :class:`UploadSession` object with the given session id.
        :rtype:
            :class`UploadSession`
        """
        return self.translator.get('upload_session')(session=self._session, object_id=session_id)

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
        return self.translator.get('comment')(session=self._session, object_id=comment_id)

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
        return self.translator.get('user')(session=self._session, object_id=user_id)

    def invite(self, invite_id):
        """
        Initialize a :class:`Invite` object, whose box id is invite_id.

        :param invite_id:
            The invite ID of the :class:`Invite` object.
        :type invite_id:
            `unicode`
        :return:
            A :class:`Invite` object with the given entry ID.
        :rtype:
            :class:`Invite`
        """
        return self.translator.get('invite')(session=self._session, object_id=invite_id)

    def email_alias(self, alias_id):
        """
        Initialize a :class: `EmailAlias` object, whose box id is alias_id.

        :param alias_id:
            The aliad id of the :class:`EmailAlias` object.
        :type alias_id:
            `unicode`
        :return:
            A :class:`EmailAlias` object with the given entry ID.
        :rtype:
            :class:`EmailAlias`
        """
        return self.translator.get('email_alias')(session=self._session, object_id=alias_id)

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
        return self.translator.get('group')(session=self._session, object_id=group_id)

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
        return self.translator.get('collaboration')(session=self._session, object_id=collab_id)

    def collaboration_whitelist(self):
        """
        Initilializes a :class:`CollaborationWhitelist` object.

        :return:
            A :class:`CollaborationWhitelist` object.
        :rype:
            :class:`CollaborationWhitelist`.
        """
        return CollaborationWhitelist(self._session)

    def collaboration_whitelist_entry(self, entry_id):
        """
        Initialize a :class:`CollaborationWhitelistEntry` object, whose box id is entry_id.

        :param entry_id:
            The box id of the :class:`CollaborationWhitelistEntry` object.
        :type entry_id:
            `unicode`
        :return:
            A :class:`CollaborationWhitelistEntry` object with the given entry id.
        :rtype:
            :class:`CollaborationWhitelistEntry`
        """
        return self.translator.get('collaboration_whitelist_entry')(session=self._session, object_id=entry_id)

    def collaboration_whitelist_exempt_target(self, exemption_id):
        """
        Initialize a :class:`CollaborationWhitelistExemptTarget` object, whose box id is target_id.

        :param exemption_id:
            The box id of the :class:`CollaborationWhitelistExemptTarget` object.
        :type exemption_id:
            `unicode`
        :return:
            A :class:`CollaborationWhitelistExemptTarget` object with the given target id.
        :rtype:
            :class:`CollaborationWhitelistExemptTarget`
        """
        return self.translator.get('collaboration_whitelist_exempt_target')(
            session=self._session,
            object_id=exemption_id
        )

    def trash(self):
        """
        Initialize a :class:`Trash` object.

        :return:
            A :class:`Trash` object.
        :rtype:
            :class:`Trash`
        """
        return Trash(self._session)

    def legal_hold_policy(self, policy_id):
        """
        Initialize a :class:`LegalHoldPolicy` object, whose box id is policy_id.

        :param policy_id:
            The box ID of the :class:`LegalHoldPolicy` object.
        :type policy_id:
            `unicode`
        :return:
            A :class:`LegalHoldPolicy` object with the given entry ID.
        :rtype:
            :class:`LegalHoldPolicy`
        """
        return self.translator.get('legal_hold_policy')(session=self._session, object_id=policy_id)

    def legal_hold_policy_assignment(self, policy_assignment_id):
        """
        Initialize a :class:`LegalHoldPolicyAssignment` object, whose box id is policy_assignment_id.

        :param policy_assignment_id:
            The assignment ID of the :class:`LegalHoldPolicyAssignment` object.
        :type policy_assignment_id:
            `unicode`
        :return:
            A :class:`LegalHoldPolicyAssignment` object with the given entry ID.
        :rtype:
            :class:`LegalHoldPolicyAssignment`
        """
        return self.translator.get('legal_hold_policy_assignment')(session=self._session, object_id=policy_assignment_id)

    def legal_hold(self, hold_id):
        """
        Initialize a :class:`LegalHold` object, whose box id is policy_id.

        :param hold_id:
            The legal hold ID of the :class:`LegalHold` object.
        :type hold_id:
            `unicode`
        :return:
            A :class:`LegalHold` object with the given entry ID.
        :rtype:
            :class:`LegalHold`
        """
        return self.translator.get('legal_hold')(session=self._session, object_id=hold_id)

    @api_call
    def create_legal_hold_policy(
            self,
            policy_name,
            description=None,
            filter_starting_at=None,
            filter_ending_at=None,
            is_ongoing=None
    ):
        """
        Create a legal hold policy.

        :param policy_name:
            The legal hold policy's display name.
        :type policy_name:
            `unicode`
        :param description:
            The description of the legal hold policy.
        :type description:
            `unicode` or None
        :param filter_starting_at:
            The start time filter for legal hold policy
        :type filter_starting_at:
            `unicode` or None
        :param filter_ending_at:
            The end time filter for legal hold policy
        :type filter_ending_at:
            `unicode` or None
        :param is_ongoing:
            After initialization, Assignments under this Policy will continue applying to
            files based on events, indefinitely.
        :type is_ongoing:
            `bool` or None
        :returns:
            A legal hold policy object
        :rtype:
            :class:`LegalHoldPolicy
        """
        url = self.get_url('legal_hold_policies')
        policy_attributes = {'policy_name': policy_name}
        if description is not None:
            policy_attributes['description'] = description
        if filter_starting_at is not None:
            policy_attributes['filter_starting_at'] = filter_starting_at
        if filter_ending_at is not None:
            policy_attributes['filter_ending_at'] = filter_ending_at
        if is_ongoing is not None:
            policy_attributes['is_ongoing'] = is_ongoing
        box_response = self._session.post(url, data=json.dumps(policy_attributes))
        response = box_response.json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def get_legal_hold_policies(self, policy_name=None, limit=None, marker=None, fields=None):
        """
        Get the entries in the legal hold policy using limit-offset paging.

        :param policy_name:
            The name of the legal hold policy case insensitive to search for
        :type policy_name:
            `unicode` or None
        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param marker:
            The paging marker to start paging from.
        :type marker:
            `unicode` or None
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries in the legal hold policy
        :rtype:
            :class:`BoxObjectCollection`
        """
        additional_params = {}
        if policy_name is not None:
            additional_params['policy_name'] = policy_name
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self.get_url('legal_hold_policies'),
            additional_params=additional_params,
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )

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
        return self.translator.get('collection')(session=self._session, object_id=collection_id)

    @api_call
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
            self.session,
            self._session.get_url('collections'),
            limit=limit,
            fields=fields,
            offset=offset,
            return_full_pages=False,
        )

    def enterprise(self, enterprise_id):
        """
        Initialize a :class:`Enterprise` object, whose box ID is enterprise_id.

        :param enterprise_id:
            The box id of the :class:`Enterprise` object.
        :type enterprise_id:
            `unicode`
        :return:
            A :class:`Enterprise` object with the given enterprise ID.
        :rtype:
            :class:`Enterprise`
        """
        return self.translator.get('enterprise')(session=self._session, object_id=enterprise_id)

    @api_call
    def get_current_enterprise(self):
        """
        Get the enterprise of the current user.

        :returns:
            The authenticated user's enterprise
        :rtype:
            :class:`Enterprise`
        """
        user = self.user().get(fields=['enterprise'])
        enterprise_object = user['enterprise']
        return self.translator.translate(
            session=self._session,
            response_object=enterprise_object,
        )

    @api_call
    def users(self, limit=None, offset=0, filter_term=None, user_type=None, fields=None, use_marker=False, marker=None):
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
        :param user_type:
            Filters the results to only users of the given type: 'managed', 'external', or 'all'.
        :type user_type:
            `unicode` or None
        :param fields:
            List of fields to request on the :class:`User` objects.
        :type fields:
            `Iterable` of `unicode`
        :param use_marker:
            Whether to use marker-based paging instead of offset-based paging, defaults to False.
        :type use_marker:
            `bool`
        :param marker:
            The paging marker to start returning items from when using marker-based paging.
        :type marker:
            `unicode` or None
        :return:
            The list of all users in the enterprise.
        :rtype:
            `Iterable` of :class:`User`
        """
        url = self.get_url('users')
        additional_params = {}
        if filter_term:
            additional_params['filter_term'] = filter_term
        if user_type:
            additional_params['user_type'] = user_type

        if use_marker:
            additional_params['usemarker'] = True
            return MarkerBasedObjectCollection(
                url=url,
                session=self._session,
                limit=limit,
                marker=marker,
                fields=fields,
                additional_params=additional_params,
                return_full_pages=False,
            )
        return LimitOffsetBasedObjectCollection(
            url=url,
            session=self._session,
            additional_params=additional_params,
            limit=limit,
            offset=offset,
            fields=fields,
            return_full_pages=False,
        )

    @api_call
    def search(self):
        """
        Get a Search object that can be used for searching Box content.

        :return:
            The Search object
        :rtype:
            :class:`Search`
        """
        return Search(self._session)

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
        return self.translator.get('group_membership')(
            session=self._session,
            object_id=group_membership_id,
        )

    @api_call
    def get_groups(self, name=None, limit=None, offset=None, fields=None):
        """
        Get a list of all groups for the current user.

        :param name:
            Filter on the name of the groups to return.
        :type name:
            `unicode` or None
        :param limit:
            The maximum number of groups to return. If not specified, the Box API will determine an appropriate limit.
        :type limit:
            `int` or None
        :param offset:
            The group index at which to start the response.
        :type offset:
            `int` or None.
        :param fields:
            List of fields to request on the :class:`Group` objects.
        :type fields:
            `Iterable` of `unicode`
        :return:
            The collection of all groups.
        :rtype:
            `Iterable` of :class:`Group`
        """
        url = self.get_url('groups')
        additional_params = {}
        if name:
            additional_params['name'] = name
        return LimitOffsetBasedObjectCollection(
            url=url,
            session=self._session,
            additional_params=additional_params,
            limit=limit,
            offset=offset,
            fields=fields,
            return_full_pages=False,
        )

    def webhook(self, webhook_id):
        """
        Initialize a :class:`Webhook` object, whose box id is webhook_id.

        :param webhook_id:
            The box ID of the :class: `Webhook` object.
        :type webhook_id:
            `unicode`
        :return:
            A :class:`Webhook` object with the given entry ID.
        :rtype:
            :class:`Webhook`
        """
        return self.translator.get('webhook')(session=self._session, object_id=webhook_id)

    @api_call
    def create_webhook(self, target, triggers, address):
        """
        Create a webhook on the given file.

        :param target:
            Either a :class:`File` or :class:`Folder` to assign a webhook to.
        :type target:
            :class:`File` or :class`Folder`
        :param triggers:
            Event types that trigger notifications for the target.
        :type triggers:
            `list` of `unicode`
        :param address:
            The url to send the notification to.
        :type address:
            `unicode`
        :return:
            A :class:`Webhook` object with the given entry ID.
        :rtype:
            :class:`Webhook`
        """
        url = self.get_url('webhooks')
        webhook_attributes = {
            'target': {
                'type': target.object_type,
                'id': target.object_id,
            },
            'triggers': triggers,
            'address': address,
        }
        box_response = self._session.post(url, data=json.dumps(webhook_attributes))
        response = box_response.json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def get_webhooks(self, limit=None, marker=None, fields=None):
        """
        Get all webhooks in an enterprise.

        :param limit:
            The maximum number of entries to return.
        :type limit:
            `int` or None
        :param marker:
            The position marker at which to begin the response.
        :type marker:
            `unicode` or None
        :param fields:
            List of fields to request on the file or folder which the `RecentItem` references.
        :type fields:
            `Iterable` of `unicode`
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
            fields=fields,
        )

    @api_call
    def create_group(
            self,
            name,
            provenance=None,
            external_sync_identifier=None,
            description=None,
            invitability_level=None,
            member_viewability_level=None,
            fields=None,
    ):
        """
        Create a group with the given name.

        :param name:
            The name of the group.
        :type name:
            `unicode`
        :param provenance:
            Used to track the external source where the group is coming from.
        :type provenance:
            `unicode` or None
        :param external_sync_identifier:
            Used as a group identifier for groups coming from an external source.
        :type external_sync_identifier:
            `unicode` or None
        :param description:
            Description of the group.
        :type description:
            `unicode` or None
        :param invitability_level:
            Specifies who can invite this group to folders.
        :type invitability_level:
            `unicode`
        :param member_viewability_level:
            Specifies who can view the members of this group.
        :type member_viewability_level:
            `unicode`
        :param fields:
            List of fields to request on the :class:`Group` objects.
        :type fields:
            `Iterable` of `unicode`
        :return:
            The newly created Group.
        :rtype:
            :class:`Group`
        :raises:
            :class:`BoxAPIException` if current user doesn't have permissions to create a group.
        """
        url = self.get_url('groups')
        additional_params = {}
        body_attributes = {
            'name': name,
        }
        if provenance is not None:
            body_attributes['provenance'] = provenance
        if external_sync_identifier is not None:
            body_attributes['external_sync_identifier'] = external_sync_identifier
        if description is not None:
            body_attributes['description'] = description
        if invitability_level is not None:
            body_attributes['invitability_level'] = invitability_level
        if member_viewability_level is not None:
            body_attributes['member_viewability_level'] = member_viewability_level
        if fields is not None:
            additional_params['fields'] = ','.join(fields)
        box_response = self._session.post(url, data=json.dumps(body_attributes), params=additional_params)
        response = box_response.json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
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
        return self.translator.get('storage_policy')(session=self._session, object_id=policy_id)

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
        return self.translator.get('storage_policy_assignment')(session=self._session, object_id=assignment_id)

    def get_storage_policies(self, limit=None, marker=None, fields=None):
        """
        Get the entries in the storage policy using marker-based paging.

        :param limit:
            The maximum number of items to return.
        :type limit:
            `int` or None
        :param marker:
            The paging marker to start returning items from when using marker-based paging.
        :type marker:
            `unicode` or None
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            Returns the storage policies available for the current enterprise.
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

    def terms_of_service(self, tos_id):
        """
        Initialize a :class:`TermsOfService` object, whose box id is tos_id.

        :param tos_id:
            The box id of the :class:`TermsOfService` object.
        :type tos_id:
            `unicode`
        :return:
            A :class:`TermsOfService` object with the given terms of service id.
        :rtype:
            :class:`TermsOfService`
        """
        return self.translator.get('terms_of_service')(session=self._session, object_id=tos_id)

    def terms_of_service_user_status(self, tos_user_status_id):
        """
        Initialize a :class:`TermsOfServiceUserStatus` object, whose box id is tos_user_status_id.

        :param tos_user_status_id:
            The box id of the :class:`TermsOfServiceUserStatus` object.
        :type tos_id:
            `unicode`
        :return:
            A :class:`TermsOfServiceUserStatus` object with the given terms of service user status id.
        :rtype:
            :class:`TermsOfServiceUserStatus`
        """
        return self.translator.get('terms_of_service_user_status')(session=self._session, object_id=tos_user_status_id)

    def get_terms_of_services(self, tos_type=None, limit=None, fields=None):
        """
        Get the entries in the terms of service using limit-offset paging.

        :param tos_type:
            Can be set to `managed` or `external` for the type of terms of service.
        :type tos_type:
            :class:`TermsOfServiceType`
        :param: limit
            The maximum number of items to return. If limit is set to None, then the default
            limit (returned by Box in the response) is used.
        :type: limit
            `int` or None
        :param fields:
            List of fields to request
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries in the terms of service
        :rtype:
            :class:`BoxObjectCollection`
        """
        additional_params = {}
        if tos_type is not None:
            additional_params['tos_type'] = tos_type
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self._session.get_url('terms_of_services'),
            additional_params=additional_params,
            limit=limit,
            marker=None,
            fields=fields,
            return_full_pages=False,
        )

    def task(self, task_id):
        """
        Initialize a :class:`Task` object, whose box id is task_id.

        :param task_id:
            The box ID of the :class:`Task` object.
        :type task_id:
            `unicode`
        :return:
            A :class:`Task` object with the given entry ID.
        :rtype:
            :class:`Task`
        """
        return self.translator.get('task')(session=self._session, object_id=task_id)

    def task_assignment(self, assignment_id):
        """
        Initialize a :class:`TaskAssignment` object, whose box id is assignment_id.

        :param assignment_id:
            The box ID of the :class:`TaskAssignment` object.
        :type assignment_id:
            `unicode`
        :return:
            A :class:`TaskAssignment` object with the given entry ID.
        :rtype:
            :class:`TaskAssignment`
        """
        return self.translator.get('task_assignment')(session=self._session, object_id=assignment_id)

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
        return self.translator.get('retention_policy')(session=self._session, object_id=retention_id)

    def file_version_retention(self, retention_id):
        """
        Initialize a :class:`FileVersionRetention` object, whose box id is retention_id.

        :param retention_id:
            The box ID of the :class:`FileVersionRetention` object.
        :type retention_id:
            `unicode`
        :return:
            A :class:`FileVersionRetention` object with the given retention ID.
        :rtype:
            :class:`FileVersionRetention`
        """
        return self.translator.get('file_version_retention')(session=self._session, object_id=retention_id)

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
        return self.translator.get('retention_policy_assignment')(session=self._session, object_id=assignment_id)

    @api_call
    def create_retention_policy(
            self,
            policy_name,
            disposition_action,
            retention_length,
            can_owner_extend_retention=None,
            are_owners_notified=None,
            custom_notification_recipients=None,
    ):
        """
        Create a retention policy for the given enterprise.

        :param policy_name:
            The name of the retention policy.
        :type policy_name:
            `unicode`
        :param retention_length:
            The amount of time in days to apply the retention policy to the selected content.
            The retention_length should be set to float('inf') for indefinite policies.
        :type retention_length:
            `int` or float('inf')
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
        :param custom_notification_recipients:
            A custom list of user mini objects that should be notified when a file is nearing expiration.
        :type custom_notification_recipients:
            `list` of :class:`User` objects
        :return:
            The newly created Retention Policy
        :rtype:
            :class:`RetentionPolicy`
        """
        url = self.get_url('retention_policies')
        user_list = []
        retention_attributes = {
            'policy_name': policy_name,
            'disposition_action': disposition_action,
        }
        if retention_length == float('inf'):
            retention_attributes['policy_type'] = 'indefinite'
        else:
            retention_attributes['policy_type'] = 'finite'
            retention_attributes['retention_length'] = retention_length
        if can_owner_extend_retention is not None:
            retention_attributes['can_owner_extend_retention'] = can_owner_extend_retention
        if are_owners_notified is not None:
            retention_attributes['are_owners_notified'] = are_owners_notified
        if custom_notification_recipients is not None:
            user_list = [{'type': user.object_type, 'id': user.object_id} for user in custom_notification_recipients]
            retention_attributes['custom_notification_recipients'] = user_list
        box_response = self._session.post(url, data=json.dumps(retention_attributes))
        response = box_response.json()
        return self.translator.translate(
            session=self._session,
            response_object=response
        )

    @api_call
    def get_retention_policies(
            self,
            policy_name=None,
            policy_type=None,
            user=None,
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
        :param user:
            A user to filter the retention policies.
        :type user:
            :class:`User` or None
        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param marker:
            The paging marker to start paging from
        :type marker:
            `unicode` or None
        :param fields:
            List of fields to request
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries in the retention policy
        :rtype:
            :class:`BoxObjectCollection`
        """
        additional_params = {}
        if policy_name is not None:
            additional_params['policy_name'] = policy_name
        if policy_type is not None:
            additional_params['policy_type'] = policy_type
        if user is not None:
            additional_params['created_by_user_id'] = user.object_id
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self._session.get_url('retention_policies'),
            additional_params=additional_params,
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )

    def create_terms_of_service(self, status, tos_type, text):
        """
        Create a terms of service.

        :param status:
            The status of the terms of service.
        :type status:
            :class:`TermsOfServiceStatus`
        :param tos_type:
            The type of the terms of service. Can be set to `managed` or `external`.
        :type tos_type:
            :class:`TermsOfServiceType`
        :param text:
            The message of the terms of service.
        :type text:
            `unicode`
        :returns:
            A newly created :class:`TermsOfService` object
        :rtype:
            :class:`TermsOfService`
        """
        url = self.get_url('terms_of_services')
        body = {
            'status': status,
            'tos_type': tos_type,
            'text': text
        }
        box_response = self._session.post(url, data=json.dumps(body))
        response = box_response.json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def get_file_version_retentions(
            self,
            target_file=None,
            file_version=None,
            policy=None,
            disposition_action=None,
            disposition_before=None,
            disposition_after=None,
            limit=None,
            marker=None,
            fields=None,
    ):
        """
        Get the entries in the file version retention.

        :param target_file:
            The file to filter the file version.
        :type target_file:
            :class:`File` or None
        :param file_version:
            A file version to filter the file version retentions by.
        :type file_version:
            :class:`FileVersion` or None
        :param policy:
            A policy to filter the file version retentions by.
        :type policy:
            :class:`RetentionPolicy` or None
        :param disposition_action:
            Can be set to `permanently_delete` or `remove_retention`.
        :type disposition_action:
            `unicode` or None
        :param disposition_before:
            A date time filter for disposition action.
        :type disposition_before:
            `unicode` or None
        :param disposition_after:
            A date time filter for disposition action.
        :type disposition_after:
            `unicode` or None
        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param marker:
            The paging marker to start paging from
        :type marker:
            `unicode` or None
        :param fields:
            List of fields to request
        :type fields:
            `Iterable` of `unicode`
        :returns:
           An iterator of the entries in the file version retention.
        :rtype:
            :class:`BoxObjectCollection`
        """
        additional_params = {}
        if target_file is not None:
            additional_params['file_id'] = target_file.object_id
        if file_version is not None:
            additional_params['file_version_id'] = file_version.object_id
        if policy is not None:
            additional_params['policy_id'] = policy.object_id
        if disposition_action is not None:
            additional_params['disposition_action'] = disposition_action
        if disposition_before is not None:
            additional_params['disposition_before'] = disposition_before
        if disposition_after is not None:
            additional_params['disposition_after'] = disposition_after
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self._session.get_url('file_version_retentions'),
            additional_params=additional_params,
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )

    def web_link(self, web_link_id):
        """
        Initialize a :class: `WebLink` object, whose box id is web_link_id.
        :param web_link_id:
            The box ID of the :class:`WebLink` object.
        :type web_link_id:
            `unicode`
        :return:
            A :class:`WebLink` object with the given entry ID.
        :rtype:
            :class:`WebLink`
        """
        return self.translator.get('web_link')(session=self._session, object_id=web_link_id)

    @api_call
    def get_recent_items(self, limit=None, marker=None, fields=None, **collection_kwargs):
        """
        Get the user's recently accessed items.

        :param: limit
            The maximum number of items to return. If limit is set to None, then the default
            limit (returned by Box in the response) is used. See https://developer.box.com/en/reference/get-recent-items/
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
        Get information about a Box shared link. https://developer.box.com/en/reference/get-shared-items/

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
            self.get_url('shared_items'),
            headers=get_shared_link_header(shared_link, password),
        ).json()
        return self.translator.translate(
            session=self._session.with_shared_link(shared_link, password),
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
            https://developer.box.com/en/reference/post-users/
        """
        url = self.get_url('users')
        user_attributes['name'] = name
        if login is not None:
            user_attributes['login'] = login
        else:
            user_attributes['is_platform_access_only'] = True
        box_response = self._session.post(url, data=json.dumps(user_attributes))
        response = box_response.json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def get_pending_collaborations(self, limit=None, offset=None, fields=None):
        """
        Get the entries in the pending collaborations using limit-offset paging.

        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param offset:
            The offset of the item at which to begin the response.
        :type offset:
            `int` or None
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries in the pending collaborations
        :rtype:
            :class:`BoxObjectCollection`
        """
        return LimitOffsetBasedObjectCollection(
            session=self._session,
            url=self.get_url('collaborations'),
            additional_params={'status': 'pending'},
            limit=limit,
            offset=offset,
            fields=fields,
            return_full_pages=False,
        )

    @api_call
    def downscope_token(self, scopes, item=None, additional_data=None, shared_link=None):
        """
        Generate a downscoped token for the provided file or folder with the provided scopes.

        :param scope:
            The scope(s) to apply to the resulting token.
        :type scopes:
            `Iterable` of :class:`TokenScope`
        :param item:
            (Optional) The file or folder to get a downscoped token for. If None and shared_link None, the resulting
            token will not be scoped down to just a single item.
        :type item:
            :class:`Item`
        :param shared_link:
            (Optional) The shared link to get a downscoped token for. If None and item None, the resulting token
            will not be scoped down to just a single item.
        :type shared_link:
            `str`
        :param additional_data:
            (Optional) Key value pairs which can be used to add/update the default data values in the request.
        :type additional_data:
            `dict`
        :return:
            The response for the downscope token request.
        :rtype:
            :class:`TokenResponse`
        """
        url = '{base_auth_url}/token'.format(base_auth_url=self._session.api_config.OAUTH2_API_URL)
        access_token = self.auth.access_token or self.auth.refresh(None)
        data = {
            'subject_token': access_token,
            'subject_token_type': 'urn:ietf:params:oauth:token-type:access_token',
            'scope': ' '.join(scopes),
            'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange',
        }

        if item:
            data['resource'] = item.get_url()
        if shared_link:
            data['box_shared_link'] = shared_link
        if additional_data:
            data.update(additional_data)

        box_response = self._session.post(url, data=data)

        return TokenResponse(box_response.json())

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

    def device_pinner(self, device_pin_id):
        """
        Initialize a :class:`DevicePinner` object, whose box id is device_pin_id.

        :param device_pin_id:
            The assignment ID of the :class:`DevicePin` object.
        :type device_pin_id:
            `unicode`
        :return:
            A :class:`DevicePinner` object with the given entry ID.
        :rtype:
            :class:`DevicePinner`
        """
        return self.translator.get('device_pinner')(session=self._session, object_id=device_pin_id)

    def device_pinners(self, enterprise=None, direction=None, limit=None, marker=None, fields=None):
        """
        Returns all of the device pins for the given enterprise.

        :param enterprise:
            The enterprise to retrieve device pinners for, defaulting to the current enterprise.
        :type enterprise:
            :class`Enterprise` or None
        :param direction:
            The sorting direction. Set to `ASC` or `DESC`
        :type direction:
            `unicode` or None
        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param marker:
            The paging marker to start paging from.
        :type marker:
            `unicode` or None
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries in the device pins.
        :rtype:
            :class:`BoxObjectCollection`
        """
        enterprise_id = enterprise.object_id if enterprise is not None else self.get_current_enterprise().id
        additional_params = {}
        if direction is not None:
            additional_params['direction'] = direction
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self.get_url('enterprises', enterprise_id, 'device_pinners'),
            additional_params=additional_params,
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )

    def metadata_cascade_policy(self, policy_id):
        """
        Initializes a :class:`MetadataCascadePolicy` object with the given policy ID.

        :param policy_id:
            The ID of the cascade policy object
        :type policy_id:
            `unicode`
        :returns:
            The cascade policy object
        :rtype:
            :class:`MetadataCascadePolicy`
        """
        return self.translator.get('metadata_cascade_policy')(
            session=self._session,
            object_id=policy_id,
        )

    def metadata_template(self, scope, template_key):
        """
        Initialize a :class:`MetadataTemplate` object with the given scope and template key.

        :param scope:
            The scope of the metadata template, e.g. 'enterprise' or 'global'
        :type scope:
            `unicode`
        :param template_key:
            The key of the metadata template
        :type template_key:
            `unicode`
        :returns:
            The metadata template object
        :rtype:
            :class:`MetadataTemplate`
        """
        return self.translator.get('metadata_template')(
            session=self._session,
            object_id=None,
            response_object={
                'type': 'metadata_template',
                'scope': scope,
                'templateKey': template_key,
            },
        )

    def metadata_template_by_id(self, template_id):
        """
        Retrieves a metadata template by ID

        :param template_id:
            The ID of the template object
        :type template_id:
            `unicode`
        :returns:
            The metadata template with data populated from the API
        :rtype:
            :class:`MetadataTemplate`
        """
        return self.translator.get('metadata_template')(
            session=self._session,
            object_id=template_id,
        )

    @api_call
    def get_metadata_templates(self, scope='enterprise', limit=None, marker=None, fields=None):
        """
        Get all metadata templates for a given scope.  By default, retrieves all metadata templates for the current
        enterprise.

        :param scope:
            The scope to retrieve templates for
        :type scope:
            `unicode`
        :type limit:
            `int` or None
        :param marker:
            The paging marker to start paging from.
        :type marker:
            `unicode` or None
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            The collection of metadata templates for the given scope
        :rtype:
            :class:`BoxObjectCollection`
        """
        return MarkerBasedObjectCollection(
            url=self._session.get_url('metadata_templates', scope),
            session=self._session,
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )

    @api_call
    def create_metadata_template(self, display_name, fields, template_key=None, hidden=False, scope='enterprise', copy_instance_on_item_copy=False):
        """
        Create a new metadata template.  By default, only the display name and fields are required; the template key
        will be automatically generated based on the display name and the template will be created in the enterprise
        scope.

        :param display_name:
            The human-readable name of the template
        :type display_name:
            `unicode`
        :param fields:
            The metadata fields for the template.
        :type fields:
            `Iterable` of :class:`MetadataField`
        :param template_key:
            An optional key for the template.  If one is not provided, it will be derived from the display name.
        :type template_key:
            `unicode`
        :param hidden:
            Whether the template should be hidden in the UI
        :type hidden:
            `bool`
        :param scope:
            The scope the template should be created in
        :type scope:
            `unicode`
        :param copy_instance_on_item_copy:
            Whether or not to include the metadata when a file or folder is copied.
        :type copy_instance_on_item_copy:
            `bool`
        """
        url = self._session.get_url('metadata_templates', 'schema')
        body = {
            'scope': scope,
            'displayName': display_name,
            'hidden': hidden,
            'fields': [field.json() for field in fields],
            'copyInstanceOnItemCopy': copy_instance_on_item_copy
        }

        if template_key is not None:
            body['templateKey'] = template_key

        response = self._session.post(url, data=json.dumps(body)).json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def __create_zip(self, name, items):
        """
        Creates a zip file containing multiple files and/or folders for later download.

        :param name:
            The name of the zip file to be created.
        :type name:
            `unicode`
        :param items:
            List of files and/or folders to be contained in the zip file.
        :type items:
            `Iterable`
        :returns:
            A dictionary representing a created zip
        :rtype:
            :class:`dict`
        """
        # pylint: disable=protected-access
        url = self._session.get_url('zip_downloads')
        zip_file_items = []
        for item in items:
            zip_file_items.append({'type': item._item_type, 'id': item.object_id})
        data = {
            'download_file_name': name,
            'items': zip_file_items
        }
        return self._session.post(url, data=json.dumps(data)).json()

    @api_call
    def download_zip(self, name, items, writeable_stream):
        """
        Downloads a zip file containing multiple files and/or folders.

        :param name:
            The name of the zip file to be created.
        :type name:
            `unicode`
        :param items:
            List of files or folders to be part of the created zip.
        :type items:
            `Iterable`
        :param writeable_stream:
            Stream to pipe the readable stream of the zip file.
        :type writeable_stream:
            `zip`
        :returns:
            A status response object
        :rtype:
            :class:`dict`
        """
        created_zip = self.__create_zip(name, items)
        response = self._session.get(created_zip['download_url'], expect_json_response=False, stream=True)
        for chunk in response.network_response.response_as_stream.stream(decode_content=True):
            writeable_stream.write(chunk)
        status = self._session.get(created_zip['status_url']).json()
        status.update(created_zip)
        return self.translator.translate(
            session=self._session,
            response_object=status,
        )
