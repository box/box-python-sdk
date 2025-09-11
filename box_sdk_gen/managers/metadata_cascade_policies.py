from enum import Enum

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.metadata_cascade_policies import MetadataCascadePolicies

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.metadata_cascade_policy import MetadataCascadePolicy

from box_sdk_gen.schemas.conflict_error import ConflictError

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import prepare_params

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.serialization.json import sd_to_json

from box_sdk_gen.serialization.json import SerializedData


class CreateMetadataCascadePolicyScope(str, Enum):
    GLOBAL = 'global'
    ENTERPRISE = 'enterprise'


class ApplyMetadataCascadePolicyConflictResolution(str, Enum):
    NONE = 'none'
    OVERWRITE = 'overwrite'


class MetadataCascadePoliciesManager:
    def __init__(
        self,
        *,
        auth: Optional[Authentication] = None,
        network_session: NetworkSession = None
    ):
        if network_session is None:
            network_session = NetworkSession()
        self.auth = auth
        self.network_session = network_session

    def get_metadata_cascade_policies(
        self,
        folder_id: str,
        *,
        owner_enterprise_id: Optional[str] = None,
        marker: Optional[str] = None,
        offset: Optional[int] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> MetadataCascadePolicies:
        """
                Retrieves a list of all the metadata cascade policies

                that are applied to a given folder. This can not be used on the root


                folder with ID `0`.

                :param folder_id: Specifies which folder to return policies for. This can not be used on the
        root folder with ID `0`.
                :type folder_id: str
                :param owner_enterprise_id: The ID of the enterprise ID for which to find metadata
        cascade policies. If not specified, it defaults to the
        current enterprise., defaults to None
                :type owner_enterprise_id: Optional[str], optional
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param offset: The offset of the item at which to begin the response.

        Queries with offset parameter value
        exceeding 10000 will be rejected
        with a 400 response., defaults to None
                :type offset: Optional[int], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'folder_id': to_string(folder_id),
                'owner_enterprise_id': to_string(owner_enterprise_id),
                'marker': to_string(marker),
                'offset': to_string(offset),
            }
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/metadata_cascade_policies',
                    ]
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, MetadataCascadePolicies)

    def create_metadata_cascade_policy(
        self,
        folder_id: str,
        scope: CreateMetadataCascadePolicyScope,
        template_key: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> MetadataCascadePolicy:
        """
                Creates a new metadata cascade policy that applies a given

                metadata template to a given folder and automatically


                cascades it down to any files within that folder.


                In order for the policy to be applied a metadata instance must first


                be applied to the folder the policy is to be applied to.

                :param folder_id: The ID of the folder to apply the policy to. This folder will
        need to already have an instance of the targeted metadata
        template applied to it.
                :type folder_id: str
                :param scope: The scope of the targeted metadata template. This template will
        need to already have an instance applied to the targeted folder.
                :type scope: CreateMetadataCascadePolicyScope
                :param template_key: The key of the targeted metadata template. This template will
        need to already have an instance applied to the targeted folder.

        In many cases the template key is automatically derived
        of its display name, for example `Contract Template` would
        become `contractTemplate`. In some cases the creator of the
        template will have provided its own template key.

        Please [list the templates for an enterprise][list], or
        get all instances on a [file][file] or [folder][folder]
        to inspect a template's key.

        [list]: e://get-metadata-templates-enterprise
        [file]: e://get-files-id-metadata
        [folder]: e://get-folders-id-metadata
                :type template_key: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'folder_id': folder_id,
            'scope': scope,
            'templateKey': template_key,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/metadata_cascade_policies',
                    ]
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, MetadataCascadePolicy)

    def get_metadata_cascade_policy_by_id(
        self,
        metadata_cascade_policy_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> MetadataCascadePolicy:
        """
                Retrieve a specific metadata cascade policy assigned to a folder.
                :param metadata_cascade_policy_id: The ID of the metadata cascade policy.
        Example: "6fd4ff89-8fc1-42cf-8b29-1890dedd26d7"
                :type metadata_cascade_policy_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/metadata_cascade_policies/',
                        to_string(metadata_cascade_policy_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, MetadataCascadePolicy)

    def delete_metadata_cascade_policy_by_id(
        self,
        metadata_cascade_policy_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Deletes a metadata cascade policy.
                :param metadata_cascade_policy_id: The ID of the metadata cascade policy.
        Example: "6fd4ff89-8fc1-42cf-8b29-1890dedd26d7"
                :type metadata_cascade_policy_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/metadata_cascade_policies/',
                        to_string(metadata_cascade_policy_id),
                    ]
                ),
                method='DELETE',
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None

    def apply_metadata_cascade_policy(
        self,
        metadata_cascade_policy_id: str,
        conflict_resolution: ApplyMetadataCascadePolicyConflictResolution,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Force the metadata on a folder with a metadata cascade policy to be applied to

                all of its children. This can be used after creating a new cascade policy to


                enforce the metadata to be cascaded down to all existing files within that


                folder.

                :param metadata_cascade_policy_id: The ID of the cascade policy to force-apply.
        Example: "6fd4ff89-8fc1-42cf-8b29-1890dedd26d7"
                :type metadata_cascade_policy_id: str
                :param conflict_resolution: Describes the desired behavior when dealing with the conflict
        where a metadata template already has an instance applied
        to a child.

        * `none` will preserve the existing value on the file
        * `overwrite` will force-apply the templates values over
          any existing values.
                :type conflict_resolution: ApplyMetadataCascadePolicyConflictResolution
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'conflict_resolution': conflict_resolution}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/metadata_cascade_policies/',
                        to_string(metadata_cascade_policy_id),
                        '/apply',
                    ]
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None
