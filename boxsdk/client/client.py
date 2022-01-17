# coding: utf-8
# pylint: disable=too-many-lines
import json
from typing import TYPE_CHECKING, Optional, Iterable, Union, Any, IO

from ..auth.oauth2 import TokenResponse
from ..session.session import Session, AuthorizedSession
from ..object.cloneable import Cloneable
from ..util.api_call_decorator import api_call
from ..object.search import Search
from ..object.events import Events
from ..object.collaboration_allowlist import CollaborationAllowlist
from ..object.trash import Trash
from ..pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection
from ..util.shared_link import get_shared_link_header
from ..util.deprecation_decorator import deprecated

if TYPE_CHECKING:
    from boxsdk import OAuth2
    from boxsdk.util.translator import Translator
    from boxsdk.object.folder import Folder
    from boxsdk.object.file import File
    from boxsdk.object.file_version import FileVersion
    from boxsdk.object.upload_session import UploadSession
    from boxsdk.object.comment import Comment
    from boxsdk.object.legal_hold import LegalHold
    from boxsdk.object.legal_hold_policy_assignment import LegalHoldPolicyAssignment
    from boxsdk.object.legal_hold_policy import LegalHoldPolicy
    from boxsdk.object.collaboration_allowlist_exempt_target import CollaborationAllowlistExemptTarget
    from boxsdk.object.collaboration_allowlist_entry import CollaborationAllowlistEntry
    from boxsdk.object.collaboration import Collaboration
    from boxsdk.object.group import Group
    from boxsdk.object.email_alias import EmailAlias
    from boxsdk.object.invite import Invite
    from boxsdk.object.user import User
    from boxsdk.object.sign_request import SignRequest
    from boxsdk.object.folder_lock import FolderLock
    from boxsdk.object.metadata_template import MetadataTemplate, MetadataField
    from boxsdk.object.metadata_cascade_policy import MetadataCascadePolicy
    from boxsdk.object.device_pinner import DevicePinner
    from boxsdk.auth.oauth2 import TokenScope
    from boxsdk.session.box_response import BoxResponse
    from boxsdk.object.item import Item
    from boxsdk.object.web_link import WebLink
    from boxsdk.object.retention_policy_assignment import RetentionPolicyAssignment
    from boxsdk.object.file_version_retention import FileVersionRetention
    from boxsdk.object.retention_policy import RetentionPolicy
    from boxsdk.object.task_assignment import TaskAssignment
    from boxsdk.object.task import Task
    from boxsdk.object.terms_of_service_user_status import TermsOfServiceUserStatus
    from boxsdk.object.terms_of_service import TermsOfService, TermsOfServiceType, TermsOfServiceStatus
    from boxsdk.object.storage_policy_assignment import StoragePolicyAssignment
    from boxsdk.object.storage_policy import StoragePolicy
    from boxsdk.object.webhook import Webhook
    from boxsdk.object.group_membership import GroupMembership
    from boxsdk.object.enterprise import Enterprise
    from boxsdk.object.collection import Collection
    from boxsdk.pagination.box_object_collection import BoxObjectCollection


class Client(Cloneable):
    unauthorized_session_class = Session
    authorized_session_class = AuthorizedSession

    def __init__(self, oauth: 'OAuth2', session: Session = None):
        """
        :param oauth:
            OAuth2 object used by the session to authorize requests.
        :param session:
            The session object to use. If None is provided then an instance of :class:`AuthorizedSession` will be used.
        """
        super().__init__()
        self._oauth = oauth
        if session is not None:
            self._session = session
        else:
            session = session or self.unauthorized_session_class()
            self._session = self.authorized_session_class(self._oauth, **session.get_constructor_kwargs())

    @property
    def auth(self) -> 'OAuth2':
        """
        Get the :class:`OAuth2` instance the client is using for auth to Box.
        """
        return self._oauth

    @property
    def session(self) -> Session:
        """
        Get the :class:`BoxSession` instance the client is using.
        """
        return self._session

    @property
    def translator(self) -> 'Translator':
        """The translator used for translating Box API JSON responses into `BaseAPIJSONObject` smart objects.
        """
        return self._session.translator

    def folder(self, folder_id: str) -> 'Folder':
        """
        Initialize a :class:`Folder` object, whose box id is folder_id.

        :param folder_id:
            The box id of the :class:`Folder` object. Can use '0' to get the root folder on Box.
        :return:
            A :class:`Folder` object with the given folder id.
        """
        return self.translator.get('folder')(session=self._session, object_id=folder_id)

    def root_folder(self) -> 'Folder':
        """
        Returns a user's root folder object.
        """
        return self.folder('0')

    def file(self, file_id: str) -> 'File':
        """
        Initialize a :class:`File` object, whose box id is file_id.

        :param file_id:
            The box id of the :class:`File` object.
        :return:
            A :class:`File` object with the given file id.
        """
        return self.translator.get('file')(session=self._session, object_id=file_id)

    def file_version(self, version_id: str) -> 'FileVersion':
        """
        Initialize a :class:`FileVersion` object, whose box id is version_id.

        :param version_id:
            The box id of the :class:`FileVersion` object.
        :return:
            A :class:`FileVersion` object with the given file version id.
        """
        return self.translator.get('file_version')(session=self._session, object_id=version_id)

    def upload_session(self, session_id: str) -> 'UploadSession':
        """
        Initialize a :class:`UploadSession` object, whose box id is session_id.

        :param session_id:
            The box id of the :class:`UploadSession` object.
        :return:
            A :class:`UploadSession` object with the given session id.
        """
        return self.translator.get('upload_session')(session=self._session, object_id=session_id)

    def comment(self, comment_id: str) -> 'Comment':
        """
        Initialize a :class:`Comment` object, whose Box ID is comment_id.

        :param comment_id:
            The Box ID of the :class:`Comment` object.
        :return:
            A :class:`Comment` object with the given comment ID.
        """
        return self.translator.get('comment')(session=self._session, object_id=comment_id)

    def user(self, user_id: str = 'me') -> 'User':
        """
        Initialize a :class:`User` object, whose box id is user_id.

        :param user_id:
            The user id of the :class:`User` object. Can use 'me' to get the User for the current/authenticated user.
        :return:
            A :class:`User` object with the given id.
        """
        return self.translator.get('user')(session=self._session, object_id=user_id)

    def invite(self, invite_id: str) -> 'Invite':
        """
        Initialize a :class:`Invite` object, whose box id is invite_id.

        :param invite_id:
            The invite ID of the :class:`Invite` object.
        :return:
            A :class:`Invite` object with the given entry ID.
        """
        return self.translator.get('invite')(session=self._session, object_id=invite_id)

    def email_alias(self, alias_id: str) -> 'EmailAlias':
        """
        Initialize a :class: `EmailAlias` object, whose box id is alias_id.

        :param alias_id:
            The aliad id of the :class:`EmailAlias` object.
        :return:
            A :class:`EmailAlias` object with the given entry ID.
        """
        return self.translator.get('email_alias')(session=self._session, object_id=alias_id)

    def group(self, group_id: str) -> 'Group':
        """
        Initialize a :class:`Group` object, whose box id is group_id.

        :param group_id:
            The box id of the :class:`Group` object.
        :return:
            A :class:`Group` object with the given group id.
        """
        return self.translator.get('group')(session=self._session, object_id=group_id)

    def collaboration(self, collab_id: str) -> 'Collaboration':
        """
        Initialize a :class:`Collaboration` object, whose box id is collab_id.

        :param collab_id:
            The box id of the :class:`Collaboration` object.
        :return:
            A :class:`Collaboration` object with the given group id.
        """
        return self.translator.get('collaboration')(session=self._session, object_id=collab_id)

    def collaboration_allowlist(self):
        """
        Initilializes a :class:`CollaborationAllowlist` object.

        :return:
            A :class:`CollaborationAllowlist` object.
        """
        return CollaborationAllowlist(self._session)

    def collaboration_allowlist_entry(self, entry_id: str) -> 'CollaborationAllowlistEntry':
        """
        Initialize a :class:`CollaborationAllowlistEntry` object, whose box id is entry_id.

        :param entry_id:
            The box id of the :class:`CollaborationAllowlistEntry` object.
        :return:
            A :class:`CollaborationAllowlistEntry` object with the given entry id.
        """
        return self.translator.get('collaboration_whitelist_entry')(session=self._session, object_id=entry_id)

    def collaboration_allowlist_exempt_target(self, exemption_id: str) -> 'CollaborationAllowlistExemptTarget':
        """
        Initialize a :class:`CollaborationAllowlistExemptTarget` object, whose box id is target_id.

        :param exemption_id:
            The box id of the :class:`CollaborationAllowlistExemptTarget` object.
        :return:
            A :class:`CollaborationAllowlistExemptTarget` object with the given target id.
        """
        return self.translator.get('collaboration_whitelist_exempt_target')(
            session=self._session,
            object_id=exemption_id
        )

    def trash(self) -> Trash:
        """
        Initialize a :class:`Trash` object.

        :return:
            A :class:`Trash` object.
        """
        return Trash(self._session)

    def legal_hold_policy(self, policy_id: str) -> 'LegalHoldPolicy':
        """
        Initialize a :class:`LegalHoldPolicy` object, whose box id is policy_id.

        :param policy_id:
            The box ID of the :class:`LegalHoldPolicy` object.
        :return:
            A :class:`LegalHoldPolicy` object with the given entry ID.
        """
        return self.translator.get('legal_hold_policy')(session=self._session, object_id=policy_id)

    def legal_hold_policy_assignment(self, policy_assignment_id: str) -> 'LegalHoldPolicyAssignment':
        """
        Initialize a :class:`LegalHoldPolicyAssignment` object, whose box id is policy_assignment_id.

        :param policy_assignment_id:
            The assignment ID of the :class:`LegalHoldPolicyAssignment` object.
        :return:
            A :class:`LegalHoldPolicyAssignment` object with the given entry ID.
        """
        return self.translator.get('legal_hold_policy_assignment')(session=self._session, object_id=policy_assignment_id)

    def legal_hold(self, hold_id: str) -> 'LegalHold':
        """
        Initialize a :class:`LegalHold` object, whose box id is policy_id.

        :param hold_id:
            The legal hold ID of the :class:`LegalHold` object.
        :return:
            A :class:`LegalHold` object with the given entry ID.
        """
        return self.translator.get('legal_hold')(session=self._session, object_id=hold_id)

    @api_call
    def create_legal_hold_policy(
            self,
            policy_name: str,
            description: Optional[str] = None,
            filter_starting_at: Optional[str] = None,
            filter_ending_at: Optional[str] = None,
            is_ongoing: Optional[bool] = None
    ) -> 'LegalHoldPolicy':
        """
        Create a legal hold policy.

        :param policy_name:
            The legal hold policy's display name.
        :param description:
            The description of the legal hold policy.
        :param filter_starting_at:
            The start time filter for legal hold policy
        :param filter_ending_at:
            The end time filter for legal hold policy
        :param is_ongoing:
            After initialization, Assignments under this Policy will continue applying to
            files based on events, indefinitely.
        :returns:
            A legal hold policy object
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
    def get_legal_hold_policies(
            self,
            policy_name: Optional[str] = None,
            limit: Optional[int] = None,
            marker: Optional[str] = None,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Get the entries in the legal hold policy using limit-offset paging.

        :param policy_name:
            The name of the legal hold policy case insensitive to search for
        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :param marker:
            The paging marker to start paging from.
        :param fields:
            List of fields to request.
        :returns:
            An iterator of the entries in the legal hold policy
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

    def collection(self, collection_id: str) -> 'Collection':
        """
        Initialize a :class:`Collection` object, whose box ID is collection_id.

        :param collection_id:
            The box id of the :class:`Collection` object.
        :return:
            A :class:`Collection` object with the given collection ID.
        """
        return self.translator.get('collection')(session=self._session, object_id=collection_id)

    @api_call
    def collections(
            self,
            limit: Optional[int] = None,
            offset: int = 0,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Get a list of collections for the current user.

        :param limit:
            The maximum number of users to return. If not specified, the Box API will determine an appropriate limit.
        :param offset:
            The user index at which to start the response.
        :param fields:
            List of fields to request.
        """
        return LimitOffsetBasedObjectCollection(
            self.session,
            self._session.get_url('collections'),
            limit=limit,
            fields=fields,
            offset=offset,
            return_full_pages=False,
        )

    def enterprise(self, enterprise_id: str) -> 'Enterprise':
        """
        Initialize a :class:`Enterprise` object, whose box ID is enterprise_id.

        :param enterprise_id:
            The box id of the :class:`Enterprise` object.
        :return:
            A :class:`Enterprise` object with the given enterprise ID.
        """
        return self.translator.get('enterprise')(session=self._session, object_id=enterprise_id)

    @api_call
    def get_current_enterprise(self) -> 'Enterprise':
        """
        Get the enterprise of the current user.

        :returns:
            The authenticated user's enterprise
        """
        user = self.user().get(fields=['enterprise'])
        enterprise_object = user['enterprise']
        return self.translator.translate(
            session=self._session,
            response_object=enterprise_object,
        )

    @api_call
    def users(
            self,
            limit: Optional[int] = None,
            offset: int = 0,
            filter_term: Optional[str] = None,
            user_type: Optional[str] = None,
            fields: Iterable[str] = None,
            use_marker: bool = False,
            marker: Optional[str] = None
    ) -> Iterable['User']:
        """
        Get a list of all users for the Enterprise along with their user_id, public_name, and login.

        :param limit:
            The maximum number of users to return. If not specified, the Box API will determine an appropriate limit.
        :param offset:
            The user index at which to start the response.
        :param filter_term:
            Filters the results to only users starting with the filter_term in either the name or the login.
        :param user_type:
            Filters the results to only users of the given type: 'managed', 'external', or 'all'.
        :param fields:
            List of fields to request on the :class:`User` objects.
        :param use_marker:
            Whether to use marker-based paging instead of offset-based paging, defaults to False.
        :param marker:
            The paging marker to start returning items from when using marker-based paging.
        :return:
            The list of all users in the enterprise.
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
    def search(self) -> Search:
        """
        Get a Search object that can be used for searching Box content.

        :return:
            The Search object
        """
        return Search(self._session)

    def events(self) -> Events:
        """
        Get an events object that can get the latest events from Box or set up a long polling event subscription.
        """
        return Events(self._session)

    def group_membership(self, group_membership_id: str) -> 'GroupMembership':
        """
        Initialize a :class:`GroupMembership` object, whose box id is group_membership_id.

        :param group_membership_id:
            The box id of the :class:`GroupMembership` object.
        :return:
            A :class:`GroupMembership` object with the given membership id.
        """
        return self.translator.get('group_membership')(
            session=self._session,
            object_id=group_membership_id,
        )

    @api_call
    def get_groups(
            self,
            name: Optional[str] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            fields: Iterable[str] = None
    ) -> Iterable['Group']:
        """
        Get a list of all groups for the current user.

        :param name:
            Filter on the name of the groups to return.
        :param limit:
            The maximum number of groups to return. If not specified, the Box API will determine an appropriate limit.
        :param offset:
            The group index at which to start the response.
        :param fields:
            List of fields to request on the :class:`Group` objects.
        :return:
            The collection of all groups.
        """
        url = self.get_url('groups')
        additional_params = {}
        if name:
            additional_params['filter_term'] = name
        return LimitOffsetBasedObjectCollection(
            url=url,
            session=self._session,
            additional_params=additional_params,
            limit=limit,
            offset=offset,
            fields=fields,
            return_full_pages=False,
        )

    def webhook(self, webhook_id: str) -> 'Webhook':
        """
        Initialize a :class:`Webhook` object, whose box id is webhook_id.

        :param webhook_id:
            The box ID of the :class: `Webhook` object.
        :return:
            A :class:`Webhook` object with the given entry ID.
        """
        return self.translator.get('webhook')(session=self._session, object_id=webhook_id)

    @api_call
    def create_webhook(self, target: Union['File', 'Folder'], triggers: Union[list, str], address: str) -> 'Webhook':
        """
        Create a webhook on the given file.

        :param target:
            Either a :class:`File` or :class:`Folder` to assign a webhook to.
        :param triggers:
            Event types that trigger notifications for the target.
        :param address:
            The url to send the notification to.
        :return:
            A :class:`Webhook` object with the given entry ID.
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
    def get_webhooks(
            self,
            limit: Optional[int] = None,
            marker: Optional[str] = None,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Get all webhooks in an enterprise.

        :param limit:
            The maximum number of entries to return.
        :param marker:
            The position marker at which to begin the response.
        :param fields:
            List of fields to request on the file or folder which the `RecentItem` references.
        :returns:
            An iterator of the entries in the webhook
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
            name: str,
            provenance: Optional[str] = None,
            external_sync_identifier: Optional[str] = None,
            description: Optional[str] = None,
            invitability_level: str = None,
            member_viewability_level: str = None,
            fields: Iterable[str] = None,
    ) -> 'Group':
        """
        Create a group with the given name.

        :param name:
            The name of the group.
        :param provenance:
            Used to track the external source where the group is coming from.
        :param external_sync_identifier:
            Used as a group identifier for groups coming from an external source.
        :param description:
            Description of the group.
        :param invitability_level:
            Specifies who can invite this group to folders.
        :param member_viewability_level:
            Specifies who can view the members of this group.
        :param fields:
            List of fields to request on the :class:`Group` objects.
        :return:
            The newly created Group.
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

    def storage_policy(self, policy_id: str) -> 'StoragePolicy':
        """
        Initialize a :class:`StoragePolicy` object, whose box id is policy_id.

        :param policy_id:
            The box ID of the :class:`StoragePolicy` object.
        :return:
            A :class:`StoragePolicy` object with the given entry ID.
        """
        return self.translator.get('storage_policy')(session=self._session, object_id=policy_id)

    def storage_policy_assignment(self, assignment_id: str) -> 'StoragePolicyAssignment':
        """
        Initialize a :class:`StoragePolicyAssignment` object, whose box id is assignment_id.

        :param assignment_id:
            The box ID of the :class:`StoragePolicyAssignment` object.
        :return:
            A :class:`StoragePolicyAssignment` object with the given entry ID.
        """
        return self.translator.get('storage_policy_assignment')(session=self._session, object_id=assignment_id)

    def get_storage_policies(
            self,
            limit: Optional[int] = None,
            marker: Optional[str] = None,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Get the entries in the storage policy using marker-based paging.

        :param limit:
            The maximum number of items to return.
        :param marker:
            The paging marker to start returning items from when using marker-based paging.
        :param fields:
            List of fields to request.
        :returns:
            Returns the storage policies available for the current enterprise.
        """
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self.get_url('storage_policies'),
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )

    def terms_of_service(self, tos_id: str) -> 'TermsOfService':
        """
        Initialize a :class:`TermsOfService` object, whose box id is tos_id.

        :param tos_id:
            The box id of the :class:`TermsOfService` object.
        :return:
            A :class:`TermsOfService` object with the given terms of service id.
        """
        return self.translator.get('terms_of_service')(session=self._session, object_id=tos_id)

    def terms_of_service_user_status(self, tos_user_status_id: str) -> 'TermsOfServiceUserStatus':
        """
        Initialize a :class:`TermsOfServiceUserStatus` object, whose box id is tos_user_status_id.

        :param tos_user_status_id:
            The box id of the :class:`TermsOfServiceUserStatus` object.
        :return:
            A :class:`TermsOfServiceUserStatus` object with the given terms of service user status id.
        """
        return self.translator.get('terms_of_service_user_status')(session=self._session, object_id=tos_user_status_id)

    def get_terms_of_services(
            self,
            tos_type: 'TermsOfServiceType' = None,
            limit: Optional[int] = None,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Get the entries in the terms of service using limit-offset paging.
        :param tos_type:
            Can be set to `managed` or `external` for the type of terms of service.
        :param limit:
            The maximum number of items to return. If limit is set to None, then the default
            limit (returned by Box in the response) is used.
        :param fields:
            List of fields to request
        :returns:
            An iterator of the entries in the terms of service
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

    def task(self, task_id: str) -> 'Task':
        """
        Initialize a :class:`Task` object, whose box id is task_id.

        :param task_id:
            The box ID of the :class:`Task` object.
        :return:
            A :class:`Task` object with the given entry ID.
        """
        return self.translator.get('task')(session=self._session, object_id=task_id)

    def task_assignment(self, assignment_id: str) -> 'TaskAssignment':
        """
        Initialize a :class:`TaskAssignment` object, whose box id is assignment_id.

        :param assignment_id:
            The box ID of the :class:`TaskAssignment` object.
        :return:
            A :class:`TaskAssignment` object with the given entry ID.
        """
        return self.translator.get('task_assignment')(session=self._session, object_id=assignment_id)

    def retention_policy(self, retention_id: str) -> 'RetentionPolicy':
        """
        Initialize a :class:`RetentionPolicy` object, whose box id is retention_id.

        :param retention_id:
            The box ID of the :class:`RetentionPolicy` object.
        :return:
            A :class:`RetentionPolicy` object with the given entry ID.
        """
        return self.translator.get('retention_policy')(session=self._session, object_id=retention_id)

    def file_version_retention(self, retention_id: str) -> 'FileVersionRetention':
        """
        Initialize a :class:`FileVersionRetention` object, whose box id is retention_id.

        :param retention_id:
            The box ID of the :class:`FileVersionRetention` object.
        :return:
            A :class:`FileVersionRetention` object with the given retention ID.
        """
        return self.translator.get('file_version_retention')(session=self._session, object_id=retention_id)

    def retention_policy_assignment(self, assignment_id: str) -> 'RetentionPolicyAssignment':
        """
        Initialize a :class:`RetentionPolicyAssignment` object, whose box id is assignment_id.

        :param assignment_id:
            The box ID of the :class:`RetentionPolicyAssignment` object.
        :return:
            A :class:`RetentionPolicyAssignment` object with the given assignment ID.
        """
        return self.translator.get('retention_policy_assignment')(session=self._session, object_id=assignment_id)

    @api_call
    def create_retention_policy(
            self,
            policy_name: str,
            disposition_action: str,
            retention_length: Union[int, float],
            can_owner_extend_retention: Optional[bool] = None,
            are_owners_notified: Optional[bool] = None,
            custom_notification_recipients: Iterable['User'] = None,
    ) -> 'RetentionPolicy':
        """
        Create a retention policy for the given enterprise.

        :param policy_name:
            The name of the retention policy.
        :param disposition_action:
            For `finite` policy can be set to `permanently delete` or `remove retention`.
            For `indefinite` policy this must be set to `remove_retention`
        :param retention_length:
            The amount of time in days to apply the retention policy to the selected content.
            The retention_length should be set to float('inf') for indefinite policies.
        :param can_owner_extend_retention:
            The owner of a file will be allowed to extend the retention if set to true.
        :param are_owners_notified:
            The owner or co-owner will get notified when a file is nearing expiration.
        :param custom_notification_recipients:
            A custom list of user mini objects that should be notified when a file is nearing expiration.
        :return:
            The newly created Retention Policy
        """
        url = self.get_url('retention_policies')
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
            policy_name: Optional[str] = None,
            policy_type: Optional[str] = None,
            user: Optional['User'] = None,
            limit: Optional[int] = None,
            marker: Optional[str] = None,
            fields: Iterable[str] = None,
    ) -> 'BoxObjectCollection':
        """
        Get the entries in the retention policy using marker-based paging.

        :param policy_name:
            The name of the retention policy.
        :param policy_type:
            Set to either `finite` or `indefinite`
        :param user:
            A user to filter the retention policies.
        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :param marker:
            The paging marker to start paging from
        :param fields:
            List of fields to request
        :returns:
            An iterator of the entries in the retention policy
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

    def create_terms_of_service(
            self,
            status: 'TermsOfServiceStatus',
            tos_type: 'TermsOfServiceType',
            text: str
    ) -> 'TermsOfService':
        """
        Create a terms of service.

        :param status:
            The status of the terms of service.
        :param tos_type:
            The type of the terms of service. Can be set to `managed` or `external`.
        :param text:
            The message of the terms of service.
        :returns:
            A newly created :class:`TermsOfService` object
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

    @deprecated("Use RetentionPolicyAssignment.get_files_under_retention "
                "or RetentionPolicyAssignment.get_file_versions_under_retention instead")
    @api_call
    def get_file_version_retentions(
            self,
            target_file: Optional['File'] = None,
            file_version: Optional['FileVersion'] = None,
            policy: Optional['RetentionPolicy'] = None,
            disposition_action: Optional[str] = None,
            disposition_before: Optional[str] = None,
            disposition_after: Optional[str] = None,
            limit: Optional[int] = None,
            marker: Optional[str] = None,
            fields: Iterable[str] = None,
    ) -> 'BoxObjectCollection':
        """
        Get the entries in the file version retention.

        :param target_file:
            The file to filter the file version.
        :param file_version:
            A file version to filter the file version retentions by.
        :param policy:
            A policy to filter the file version retentions by.
        :param disposition_action:
            Can be set to `permanently_delete` or `remove_retention`.
        :param disposition_before:
            A date time filter for disposition action.
        :param disposition_after:
            A date time filter for disposition action.
        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :param marker:
            The paging marker to start paging from
        :param fields:
            List of fields to request
        :returns:
           An iterator of the entries in the file version retention.
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

    def web_link(self, web_link_id: str) -> 'WebLink':
        """
        Initialize a :class: `WebLink` object, whose box id is web_link_id.
        :param web_link_id:
            The box ID of the :class:`WebLink` object.
        :return:
            A :class:`WebLink` object with the given entry ID.
        """
        return self.translator.get('web_link')(session=self._session, object_id=web_link_id)

    @api_call
    def get_recent_items(
            self,
            limit: Optional[int] = None,
            marker: Optional[str] = None,
            fields: Iterable[str] = None,
            **collection_kwargs: Any
    ) -> MarkerBasedObjectCollection:
        """
        Get the user's recently accessed items.

        :param limit:
            The maximum number of items to return. If limit is set to None, then the default
            limit (returned by Box in the response) is used. See https://developer.box.com/en/reference/get-recent-items/
            for default.
        :param marker:
            The index at which to start returning items.
        :param fields:
            List of fields to request on the file or folder which the `RecentItem` references.
        :param collection_kwargs:
            Keyword arguments passed to `MarkerBasedObjectCollection`.
        :returns:
            An iterator on the user's recent items
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
    def get_shared_item(self, shared_link: str, password: str = None) -> 'Item':
        """
        Get information about a Box shared link. https://developer.box.com/en/reference/get-shared-items/

        :param shared_link:
            The shared link.
        :param password:
            The password for the shared link.
        :return:
            The item referred to by the shared link.
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
    def make_request(self, method: str, url: str, **kwargs: Any) -> 'BoxResponse':
        """
        Make an authenticated request to the Box API.

        :param method:
            The HTTP verb to use for the request.
        :param url:
            The URL for the request.
        :return:
            The network response for the given request.
        :raises:
            :class:`BoxAPIException`
        """
        return self._session.request(method, url, **kwargs)

    @api_call
    def create_user(self, name: str, login: Optional[str] = None, **user_attributes: Any) -> 'User':
        """
        Create a new user. Can only be used if the current user is an enterprise admin, or the current authorization
        scope is a Box developer edition instance.

        :param name:
            The user's display name.
        :param login:
            The user's email address. Required for an enterprise user, but None for an app user.
        :param user_attributes:
            Additional attributes for the user. See the documentation at
            https://developer.box.com/en/reference/post-users/
        :return
            Newly created user
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
    def get_pending_collaborations(
            self,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Get the entries in the pending collaborations using limit-offset paging.

        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :param offset:
            The offset of the item at which to begin the response.
        :param fields:
            List of fields to request.
        :returns:
            An iterator of the entries in the pending collaborations
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
    def downscope_token(
            self,
            scopes: Iterable['TokenScope'],
            item: 'Item' = None,
            additional_data: dict = None,
            shared_link: str = None
    ) -> TokenResponse:
        """
        Generate a downscoped token for the provided file or folder with the provided scopes.

        :param scopes:
            The scope(s) to apply to the resulting token.
        :param item:
            (Optional) The file or folder to get a downscoped token for. If None and shared_link None, the resulting
            token will not be scoped down to just a single item.
        :param additional_data:
            (Optional) Key value pairs which can be used to add/update the default data values in the request.
        :param shared_link:
            (Optional) The shared link to get a downscoped token for. If None and item None, the resulting token
            will not be scoped down to just a single item.
        :return:
            The response for the downscope token request.
        """
        url = f'{self._session.api_config.OAUTH2_API_URL}/token'
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

    def clone(self, session: 'Session' = None) -> 'Client':
        """Base class override."""
        return self.__class__(oauth=self._oauth, session=(session or self._session))

    def get_url(self, endpoint: str, *args: Any) -> str:
        """
        Return the URL for the given Box API endpoint.

        :param endpoint:
            The name of the endpoint.
        :param args:
            Additional parts of the endpoint URL.
        """
        # pylint:disable=no-self-use
        return self._session.get_url(endpoint, *args)

    def device_pinner(self, device_pin_id: str) -> 'DevicePinner':
        """
        Initialize a :class:`DevicePinner` object, whose box id is device_pin_id.

        :param device_pin_id:
            The assignment ID of the :class:`DevicePin` object.
        :return:
            A :class:`DevicePinner` object with the given entry ID.
        """
        return self.translator.get('device_pinner')(session=self._session, object_id=device_pin_id)

    def device_pinners(
            self,
            enterprise: Optional['Enterprise'] = None,
            direction: Optional[str] = None,
            limit: Optional[int] = None,
            marker: Optional[str] = None,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Returns all of the device pins for the given enterprise.

        :param enterprise:
            The enterprise to retrieve device pinners for, defaulting to the current enterprise.
        :param direction:
            The sorting direction. Set to `ASC` or `DESC`
        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :param marker:
            The paging marker to start paging from.
        :param fields:
            List of fields to request.
        :returns:
            An iterator of the entries in the device pins.
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

    def metadata_cascade_policy(self, policy_id: str) -> 'MetadataCascadePolicy':
        """
        Initializes a :class:`MetadataCascadePolicy` object with the given policy ID.

        :param policy_id:
            The ID of the cascade policy object
        :returns:
            The cascade policy object
        """
        return self.translator.get('metadata_cascade_policy')(
            session=self._session,
            object_id=policy_id,
        )

    def metadata_template(self, scope: str, template_key: str) -> 'MetadataTemplate':
        """
        Initialize a :class:`MetadataTemplate` object with the given scope and template key.

        :param scope:
            The scope of the metadata template, e.g. 'enterprise' or 'global'
        :param template_key:
            The key of the metadata template
        :returns:
            The metadata template object
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

    def metadata_template_by_id(self, template_id: str) -> 'MetadataTemplate':
        """
        Retrieves a metadata template by ID

        :param template_id:
            The ID of the template object
        :returns:
            The metadata template with data populated from the API
        """
        return self.translator.get('metadata_template')(
            session=self._session,
            object_id=template_id,
        )

    @api_call
    def get_metadata_templates(
            self,
            scope: str = 'enterprise',
            limit: Optional[int] = None,
            marker: Optional[str] = None,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Get all metadata templates for a given scope.  By default, retrieves all metadata templates for the current
        enterprise.

        :param scope:
            The scope to retrieve templates for
        :param limit:
            The maximum number of entries to return per page.
        :param marker:
            The paging marker to start paging from.
        :param fields:
            List of fields to request.
        :returns:
            The collection of metadata templates for the given scope
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
    def create_metadata_template(
            self,
            display_name: str,
            fields: Iterable['MetadataField'],
            template_key: str = None,
            hidden: bool = False,
            scope: str = 'enterprise',
            copy_instance_on_item_copy: bool = False
    ) -> 'MetadataTemplate':
        """
        Create a new metadata template.  By default, only the display name and fields are required; the template key
        will be automatically generated based on the display name and the template will be created in the enterprise
        scope.

        :param display_name:
            The human-readable name of the template
        :param fields:
            The metadata fields for the template.
        :param template_key:
            An optional key for the template.  If one is not provided, it will be derived from the display name.
        :param hidden:
            Whether the template should be hidden in the UI
        :param scope:
            The scope the template should be created in
        :param copy_instance_on_item_copy:
            Whether or not to include the metadata when a file or folder is copied.
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
    def __create_zip(self, name: str, items: Iterable) -> dict:
        """
        Creates a zip file containing multiple files and/or folders for later download.

        :param name:
            The name of the zip file to be created.
        :param items:
            List of files and/or folders to be contained in the zip file.
        :returns:
            A dictionary representing a created zip
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
    def download_zip(self, name: str, items: Iterable, writeable_stream: IO) -> dict:
        """
        Downloads a zip file containing multiple files and/or folders.

        :param name:
            The name of the zip file to be created.
        :param items:
            List of files or folders to be part of the created zip.
        :param writeable_stream:
            Stream to pipe the readable stream of the zip file.
        :returns:
            A status response object
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

    def folder_lock(self, folder_lock_id: str) -> 'FolderLock':
        """
        Initialize a :class:`FolderLock` object, whose box id is folder_lock_id.

        :param folder_lock_id:
            The ID of the :class:`FolderLock` object.
        :return:
            A :class:`FolderLock` object with the given entry ID.
        """
        return self.translator.get('folder_lock')(session=self._session, object_id=folder_lock_id)

    def sign_request(self, sign_request_id: str) -> 'SignRequest':
        """
        Initialize a :class:`SignRequest` object, whose box id is sign_request_id.

        :param sign_request_id:
            The box id of the :class:`SignRequest` object.
        :return:
            A :class:`SignRequest` object with the given file id.
        """
        return self.translator.get('sign_request')(session=self._session, object_id=sign_request_id)

    @api_call
    def create_sign_request(
            self,
            files: Iterable,
            signers: Iterable,
            parent_folder_id: str,
            prefill_tags: Optional[Iterable] = None,
            are_reminders_enabled: Optional[bool] = None,
            are_text_signatures_enabled: Optional[bool] = None,
            days_valid: Optional[str] = None,
            email_message: Optional[Iterable] = None,
            email_subject: Optional[str] = None,
            external_id: Optional[str] = None,
            is_document_preparation_needed: Optional[bool] = None
    ) -> dict:
        """
        Used to create a new sign request.

        :param files:
            List of files to create a signing document from.
        :param signers:
            List of signers for the sign request. 35 is the max number of signers permitted.
        :param parent_folder_id:
            The id of the destination folder to place sign request specific data in.
        :param prefill_tags:
            When a document contains sign related tags in the content,
            you can prefill them using this prefill_tags by referencing the 'id' of the tag as the external_id field of the prefill tag.
        :param are_reminders_enabled:
            Reminds signers to sign a document on day 3, 8, 13 and 18. Reminders are only sent to outstanding signers.
        :param are_text_signatures_enabled:
            Disables the usage of signatures generated by typing (text).
        :param days_valid:
            Number of days after which this request will automatically expire if not completed.
        :param email_message:
            Message to include in sign request email. The field is cleaned through sanitization of specific characters.
            However, some html tags are allowed. Links included in the message are also converted to hyperlinks in the email.
            The message may contain the following html tags including a, abbr, acronym, b, blockquote, code, em, i, ul, li, ol, and strong.
            Be aware that when the text to html ratio is too high, the email may end up in spam filters. Custom styles on these tags are not allowed.
            If this field is not passed, a default message will be used.
        :param email_subject:
            Subject of sign request email. This is cleaned by sign request. If this field is not passed, a default subject will be used.
        :param external_id:
            This can be used to reference an ID in an external system that the sign request is related to.
        :param is_document_preparation_needed:
            Indicates if the sender should receive a prepare_url in the response to complete document preparation via UI.
        :returns:
            A dictionary representing a created SignRequest
        """
        url = self._session.get_url('sign_requests')

        body = {
            'source_files': files,
            'signers': signers,
            'parent_folder': {
                'id': parent_folder_id,
                'type': 'folder'
            }
        }

        if prefill_tags:
            body['prefill_tags'] = prefill_tags
        if are_reminders_enabled:
            body['are_reminders_enabled'] = are_reminders_enabled
        if are_text_signatures_enabled:
            body['are_text_signatures_enabled'] = are_text_signatures_enabled
        if days_valid:
            body['days_valid'] = days_valid
        if email_message:
            body['email_message'] = email_message
        if email_subject:
            body['email_subject'] = email_subject
        if external_id:
            body['external_id'] = external_id
        if is_document_preparation_needed:
            body['is_document_preparation_needed'] = is_document_preparation_needed

        box_response = self._session.post(url, data=json.dumps(body))
        response = box_response.json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def get_sign_requests(
            self,
            limit: Optional[int] = None,
            marker: Optional[str] = None,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Returns all the sign requests.

        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :param marker:
            The paging marker to start paging from.
        :param fields:
            List of fields to request.
        :returns:
            An iterator of the entries in the device pins.
        """
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self.get_url('sign_requests'),
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )
