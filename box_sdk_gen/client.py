from typing import Dict

from box_sdk_gen.managers.authorization import AuthorizationManager

from box_sdk_gen.managers.files import FilesManager

from box_sdk_gen.managers.trashed_files import TrashedFilesManager

from box_sdk_gen.managers.app_item_associations import AppItemAssociationsManager

from box_sdk_gen.managers.downloads import DownloadsManager

from box_sdk_gen.managers.uploads import UploadsManager

from box_sdk_gen.managers.chunked_uploads import ChunkedUploadsManager

from box_sdk_gen.managers.list_collaborations import ListCollaborationsManager

from box_sdk_gen.managers.comments import CommentsManager

from box_sdk_gen.managers.tasks import TasksManager

from box_sdk_gen.managers.file_versions import FileVersionsManager

from box_sdk_gen.managers.file_metadata import FileMetadataManager

from box_sdk_gen.managers.file_classifications import FileClassificationsManager

from box_sdk_gen.managers.skills import SkillsManager

from box_sdk_gen.managers.file_watermarks import FileWatermarksManager

from box_sdk_gen.managers.file_requests import FileRequestsManager

from box_sdk_gen.managers.folders import FoldersManager

from box_sdk_gen.managers.trashed_folders import TrashedFoldersManager

from box_sdk_gen.managers.folder_metadata import FolderMetadataManager

from box_sdk_gen.managers.folder_classifications import FolderClassificationsManager

from box_sdk_gen.managers.trashed_items import TrashedItemsManager

from box_sdk_gen.managers.folder_watermarks import FolderWatermarksManager

from box_sdk_gen.managers.folder_locks import FolderLocksManager

from box_sdk_gen.managers.metadata_templates import MetadataTemplatesManager

from box_sdk_gen.managers.classifications import ClassificationsManager

from box_sdk_gen.managers.metadata_cascade_policies import (
    MetadataCascadePoliciesManager,
)

from box_sdk_gen.managers.search import SearchManager

from box_sdk_gen.managers.user_collaborations import UserCollaborationsManager

from box_sdk_gen.managers.task_assignments import TaskAssignmentsManager

from box_sdk_gen.managers.shared_links_files import SharedLinksFilesManager

from box_sdk_gen.managers.shared_links_folders import SharedLinksFoldersManager

from box_sdk_gen.managers.web_links import WebLinksManager

from box_sdk_gen.managers.trashed_web_links import TrashedWebLinksManager

from box_sdk_gen.managers.shared_links_web_links import SharedLinksWebLinksManager

from box_sdk_gen.managers.shared_links_app_items import SharedLinksAppItemsManager

from box_sdk_gen.managers.users import UsersManager

from box_sdk_gen.managers.session_termination import SessionTerminationManager

from box_sdk_gen.managers.avatars import AvatarsManager

from box_sdk_gen.managers.transfer import TransferManager

from box_sdk_gen.managers.email_aliases import EmailAliasesManager

from box_sdk_gen.managers.memberships import MembershipsManager

from box_sdk_gen.managers.invites import InvitesManager

from box_sdk_gen.managers.groups import GroupsManager

from box_sdk_gen.managers.webhooks import WebhooksManager

from box_sdk_gen.managers.events import EventsManager

from box_sdk_gen.managers.collections import CollectionsManager

from box_sdk_gen.managers.recent_items import RecentItemsManager

from box_sdk_gen.managers.retention_policies import RetentionPoliciesManager

from box_sdk_gen.managers.retention_policy_assignments import (
    RetentionPolicyAssignmentsManager,
)

from box_sdk_gen.managers.legal_hold_policies import LegalHoldPoliciesManager

from box_sdk_gen.managers.legal_hold_policy_assignments import (
    LegalHoldPolicyAssignmentsManager,
)

from box_sdk_gen.managers.file_version_retentions import FileVersionRetentionsManager

from box_sdk_gen.managers.file_version_legal_holds import FileVersionLegalHoldsManager

from box_sdk_gen.managers.shield_information_barriers import (
    ShieldInformationBarriersManager,
)

from box_sdk_gen.managers.shield_information_barrier_reports import (
    ShieldInformationBarrierReportsManager,
)

from box_sdk_gen.managers.shield_information_barrier_segments import (
    ShieldInformationBarrierSegmentsManager,
)

from box_sdk_gen.managers.shield_information_barrier_segment_members import (
    ShieldInformationBarrierSegmentMembersManager,
)

from box_sdk_gen.managers.shield_information_barrier_segment_restrictions import (
    ShieldInformationBarrierSegmentRestrictionsManager,
)

from box_sdk_gen.managers.device_pinners import DevicePinnersManager

from box_sdk_gen.managers.terms_of_services import TermsOfServicesManager

from box_sdk_gen.managers.terms_of_service_user_statuses import (
    TermsOfServiceUserStatusesManager,
)

from box_sdk_gen.managers.collaboration_allowlist_entries import (
    CollaborationAllowlistEntriesManager,
)

from box_sdk_gen.managers.collaboration_allowlist_exempt_targets import (
    CollaborationAllowlistExemptTargetsManager,
)

from box_sdk_gen.managers.storage_policies import StoragePoliciesManager

from box_sdk_gen.managers.storage_policy_assignments import (
    StoragePolicyAssignmentsManager,
)

from box_sdk_gen.managers.zip_downloads import ZipDownloadsManager

from box_sdk_gen.managers.sign_requests import SignRequestsManager

from box_sdk_gen.managers.workflows import WorkflowsManager

from box_sdk_gen.managers.sign_templates import SignTemplatesManager

from box_sdk_gen.managers.integration_mappings import IntegrationMappingsManager

from box_sdk_gen.managers.ai import AiManager

from box_sdk_gen.managers.ai_studio import AiStudioManager

from box_sdk_gen.managers.docgen_template import DocgenTemplateManager

from box_sdk_gen.managers.docgen import DocgenManager

from box_sdk_gen.managers.enterprise_configurations import (
    EnterpriseConfigurationsManager,
)

from box_sdk_gen.managers.hubs import HubsManager

from box_sdk_gen.managers.hub_collaborations import HubCollaborationsManager

from box_sdk_gen.managers.hub_items import HubItemsManager

from box_sdk_gen.managers.shield_lists import ShieldListsManager

from box_sdk_gen.managers.archives import ArchivesManager

from box_sdk_gen.managers.external_users import ExternalUsersManager

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.networking.base_urls import BaseUrls

from box_sdk_gen.networking.proxy_config import ProxyConfig


class BoxClient:
    def __init__(self, auth: Authentication, *, network_session: NetworkSession = None):
        if network_session is None:
            network_session = NetworkSession(base_urls=BaseUrls())
        self.auth = auth
        self.network_session = network_session
        self.authorization = AuthorizationManager(
            auth=self.auth, network_session=self.network_session
        )
        self.files = FilesManager(auth=self.auth, network_session=self.network_session)
        self.trashed_files = TrashedFilesManager(
            auth=self.auth, network_session=self.network_session
        )
        self.app_item_associations = AppItemAssociationsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.downloads = DownloadsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.uploads = UploadsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.chunked_uploads = ChunkedUploadsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.list_collaborations = ListCollaborationsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.comments = CommentsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.tasks = TasksManager(auth=self.auth, network_session=self.network_session)
        self.file_versions = FileVersionsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.file_metadata = FileMetadataManager(
            auth=self.auth, network_session=self.network_session
        )
        self.file_classifications = FileClassificationsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.skills = SkillsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.file_watermarks = FileWatermarksManager(
            auth=self.auth, network_session=self.network_session
        )
        self.file_requests = FileRequestsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.folders = FoldersManager(
            auth=self.auth, network_session=self.network_session
        )
        self.trashed_folders = TrashedFoldersManager(
            auth=self.auth, network_session=self.network_session
        )
        self.folder_metadata = FolderMetadataManager(
            auth=self.auth, network_session=self.network_session
        )
        self.folder_classifications = FolderClassificationsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.trashed_items = TrashedItemsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.folder_watermarks = FolderWatermarksManager(
            auth=self.auth, network_session=self.network_session
        )
        self.folder_locks = FolderLocksManager(
            auth=self.auth, network_session=self.network_session
        )
        self.metadata_templates = MetadataTemplatesManager(
            auth=self.auth, network_session=self.network_session
        )
        self.classifications = ClassificationsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.metadata_cascade_policies = MetadataCascadePoliciesManager(
            auth=self.auth, network_session=self.network_session
        )
        self.search = SearchManager(
            auth=self.auth, network_session=self.network_session
        )
        self.user_collaborations = UserCollaborationsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.task_assignments = TaskAssignmentsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.shared_links_files = SharedLinksFilesManager(
            auth=self.auth, network_session=self.network_session
        )
        self.shared_links_folders = SharedLinksFoldersManager(
            auth=self.auth, network_session=self.network_session
        )
        self.web_links = WebLinksManager(
            auth=self.auth, network_session=self.network_session
        )
        self.trashed_web_links = TrashedWebLinksManager(
            auth=self.auth, network_session=self.network_session
        )
        self.shared_links_web_links = SharedLinksWebLinksManager(
            auth=self.auth, network_session=self.network_session
        )
        self.shared_links_app_items = SharedLinksAppItemsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.users = UsersManager(auth=self.auth, network_session=self.network_session)
        self.session_termination = SessionTerminationManager(
            auth=self.auth, network_session=self.network_session
        )
        self.avatars = AvatarsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.transfer = TransferManager(
            auth=self.auth, network_session=self.network_session
        )
        self.email_aliases = EmailAliasesManager(
            auth=self.auth, network_session=self.network_session
        )
        self.memberships = MembershipsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.invites = InvitesManager(
            auth=self.auth, network_session=self.network_session
        )
        self.groups = GroupsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.webhooks = WebhooksManager(
            auth=self.auth, network_session=self.network_session
        )
        self.events = EventsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.collections = CollectionsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.recent_items = RecentItemsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.retention_policies = RetentionPoliciesManager(
            auth=self.auth, network_session=self.network_session
        )
        self.retention_policy_assignments = RetentionPolicyAssignmentsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.legal_hold_policies = LegalHoldPoliciesManager(
            auth=self.auth, network_session=self.network_session
        )
        self.legal_hold_policy_assignments = LegalHoldPolicyAssignmentsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.file_version_retentions = FileVersionRetentionsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.file_version_legal_holds = FileVersionLegalHoldsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.shield_information_barriers = ShieldInformationBarriersManager(
            auth=self.auth, network_session=self.network_session
        )
        self.shield_information_barrier_reports = (
            ShieldInformationBarrierReportsManager(
                auth=self.auth, network_session=self.network_session
            )
        )
        self.shield_information_barrier_segments = (
            ShieldInformationBarrierSegmentsManager(
                auth=self.auth, network_session=self.network_session
            )
        )
        self.shield_information_barrier_segment_members = (
            ShieldInformationBarrierSegmentMembersManager(
                auth=self.auth, network_session=self.network_session
            )
        )
        self.shield_information_barrier_segment_restrictions = (
            ShieldInformationBarrierSegmentRestrictionsManager(
                auth=self.auth, network_session=self.network_session
            )
        )
        self.device_pinners = DevicePinnersManager(
            auth=self.auth, network_session=self.network_session
        )
        self.terms_of_services = TermsOfServicesManager(
            auth=self.auth, network_session=self.network_session
        )
        self.terms_of_service_user_statuses = TermsOfServiceUserStatusesManager(
            auth=self.auth, network_session=self.network_session
        )
        self.collaboration_allowlist_entries = CollaborationAllowlistEntriesManager(
            auth=self.auth, network_session=self.network_session
        )
        self.collaboration_allowlist_exempt_targets = (
            CollaborationAllowlistExemptTargetsManager(
                auth=self.auth, network_session=self.network_session
            )
        )
        self.storage_policies = StoragePoliciesManager(
            auth=self.auth, network_session=self.network_session
        )
        self.storage_policy_assignments = StoragePolicyAssignmentsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.zip_downloads = ZipDownloadsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.sign_requests = SignRequestsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.workflows = WorkflowsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.sign_templates = SignTemplatesManager(
            auth=self.auth, network_session=self.network_session
        )
        self.integration_mappings = IntegrationMappingsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.ai = AiManager(auth=self.auth, network_session=self.network_session)
        self.ai_studio = AiStudioManager(
            auth=self.auth, network_session=self.network_session
        )
        self.docgen_template = DocgenTemplateManager(
            auth=self.auth, network_session=self.network_session
        )
        self.docgen = DocgenManager(
            auth=self.auth, network_session=self.network_session
        )
        self.enterprise_configurations = EnterpriseConfigurationsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.hubs = HubsManager(auth=self.auth, network_session=self.network_session)
        self.hub_collaborations = HubCollaborationsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.hub_items = HubItemsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.shield_lists = ShieldListsManager(
            auth=self.auth, network_session=self.network_session
        )
        self.archives = ArchivesManager(
            auth=self.auth, network_session=self.network_session
        )
        self.external_users = ExternalUsersManager(
            auth=self.auth, network_session=self.network_session
        )

    def make_request(self, fetch_options: FetchOptions) -> FetchResponse:
        """
        Make a custom http request using the client authentication and network session.
        :param fetch_options: Options to be passed to the fetch call
        :type fetch_options: FetchOptions
        """
        auth: Authentication = (
            self.auth if fetch_options.auth == None else fetch_options.auth
        )
        network_session: NetworkSession = (
            self.network_session
            if fetch_options.network_session == None
            else fetch_options.network_session
        )
        enriched_fetch_options: FetchOptions = FetchOptions(
            auth=auth,
            network_session=network_session,
            url=fetch_options.url,
            method=fetch_options.method,
            params=fetch_options.params,
            headers=fetch_options.headers,
            data=fetch_options.data,
            file_stream=fetch_options.file_stream,
            multipart_data=fetch_options.multipart_data,
            content_type=fetch_options.content_type,
            response_format=fetch_options.response_format,
            follow_redirects=fetch_options.follow_redirects,
        )
        return network_session.network_client.fetch(enriched_fetch_options)

    def with_as_user_header(self, user_id: str) -> 'BoxClient':
        """
        Create a new client to impersonate user with the provided ID. All calls made with the new client will be made in context of the impersonated user, leaving the original client unmodified.
        :param user_id: ID of an user to impersonate
        :type user_id: str
        """
        return BoxClient(
            auth=self.auth,
            network_session=self.network_session.with_additional_headers(
                {'As-User': user_id}
            ),
        )

    def with_suppressed_notifications(self) -> 'BoxClient':
        """
        Create a new client with suppressed notifications. Calls made with the new client will not trigger email or webhook notifications
        """
        return BoxClient(
            auth=self.auth,
            network_session=self.network_session.with_additional_headers(
                {'Box-Notifications': 'off'}
            ),
        )

    def with_extra_headers(
        self, *, extra_headers: Dict[str, str] = None
    ) -> 'BoxClient':
        """
        Create a new client with a custom set of headers that will be included in every API call
        :param extra_headers: Custom set of headers that will be included in every API call, defaults to None
        :type extra_headers: Dict[str, str], optional
        """
        if extra_headers is None:
            extra_headers = {}
        return BoxClient(
            auth=self.auth,
            network_session=self.network_session.with_additional_headers(extra_headers),
        )

    def with_custom_base_urls(self, base_urls: BaseUrls) -> 'BoxClient':
        """
        Create a new client with a custom set of base urls that will be used for every API call
        :param base_urls: Custom set of base urls that will be used for every API call
        :type base_urls: BaseUrls
        """
        return BoxClient(
            auth=self.auth,
            network_session=self.network_session.with_custom_base_urls(base_urls),
        )

    def with_proxy(self, config: ProxyConfig) -> 'BoxClient':
        """
        Create a new client with a custom proxy that will be used for every API call
        """
        return BoxClient(
            auth=self.auth, network_session=self.network_session.with_proxy(config)
        )
