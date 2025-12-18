from typing import Optional

from typing import Dict

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.internal.utils import to_string

from typing import List

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.metadata_taxonomy import MetadataTaxonomy

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.metadata_taxonomies import MetadataTaxonomies

from box_sdk_gen.schemas.metadata_taxonomy_levels import MetadataTaxonomyLevels

from box_sdk_gen.schemas.metadata_taxonomy_level import MetadataTaxonomyLevel

from box_sdk_gen.schemas.metadata_taxonomy_nodes import MetadataTaxonomyNodes

from box_sdk_gen.schemas.metadata_taxonomy_node import MetadataTaxonomyNode

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import prepare_params

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.serialization.json import SerializedData

from box_sdk_gen.serialization.json import sd_to_json


class MetadataTaxonomiesManager:
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

    def create_metadata_taxonomy(
        self,
        display_name: str,
        namespace: str,
        *,
        key: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> MetadataTaxonomy:
        """
                Creates a new metadata taxonomy that can be used in

                metadata templates.

                :param display_name: The display name of the taxonomy.
                :type display_name: str
                :param namespace: The namespace of the metadata taxonomy to create.
                :type namespace: str
                :param key: The taxonomy key. If it is not provided in the request body, it will be
        generated from the `displayName`. The `displayName` would be converted
        to lower case, and all spaces and non-alphanumeric characters replaced
        with underscores., defaults to None
                :type key: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'key': key,
            'displayName': display_name,
            'namespace': namespace,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/metadata_taxonomies',
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
        return deserialize(response.data, MetadataTaxonomy)

    def get_metadata_taxonomies(
        self,
        namespace: str,
        *,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> MetadataTaxonomies:
        """
                Used to retrieve all metadata taxonomies in a namespace.
                :param namespace: The namespace of the metadata taxonomy.
        Example: "enterprise_123456"
                :type namespace: str
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {'marker': to_string(marker), 'limit': to_string(limit)}
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/metadata_taxonomies/',
                        to_string(namespace),
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
        return deserialize(response.data, MetadataTaxonomies)

    def get_metadata_taxonomy_by_key(
        self,
        namespace: str,
        taxonomy_key: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> MetadataTaxonomy:
        """
                Used to retrieve a metadata taxonomy by taxonomy key.
                :param namespace: The namespace of the metadata taxonomy.
        Example: "enterprise_123456"
                :type namespace: str
                :param taxonomy_key: The key of the metadata taxonomy.
        Example: "geography"
                :type taxonomy_key: str
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
                        '/2.0/metadata_taxonomies/',
                        to_string(namespace),
                        '/',
                        to_string(taxonomy_key),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, MetadataTaxonomy)

    def update_metadata_taxonomy(
        self,
        namespace: str,
        taxonomy_key: str,
        display_name: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> MetadataTaxonomy:
        """
                Updates an existing metadata taxonomy.
                :param namespace: The namespace of the metadata taxonomy.
        Example: "enterprise_123456"
                :type namespace: str
                :param taxonomy_key: The key of the metadata taxonomy.
        Example: "geography"
                :type taxonomy_key: str
                :param display_name: The display name of the taxonomy.
                :type display_name: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'displayName': display_name}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/metadata_taxonomies/',
                        to_string(namespace),
                        '/',
                        to_string(taxonomy_key),
                    ]
                ),
                method='PATCH',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, MetadataTaxonomy)

    def delete_metadata_taxonomy(
        self,
        namespace: str,
        taxonomy_key: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Delete a metadata taxonomy.

                This deletion is permanent and cannot be reverted.

                :param namespace: The namespace of the metadata taxonomy.
        Example: "enterprise_123456"
                :type namespace: str
                :param taxonomy_key: The key of the metadata taxonomy.
        Example: "geography"
                :type taxonomy_key: str
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
                        '/2.0/metadata_taxonomies/',
                        to_string(namespace),
                        '/',
                        to_string(taxonomy_key),
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

    def create_metadata_taxonomy_level(
        self,
        namespace: str,
        taxonomy_key: str,
        request_body: List[MetadataTaxonomyLevel],
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> MetadataTaxonomyLevels:
        """
                Creates new metadata taxonomy levels.
                :param namespace: The namespace of the metadata taxonomy.
        Example: "enterprise_123456"
                :type namespace: str
                :param taxonomy_key: The key of the metadata taxonomy.
        Example: "geography"
                :type taxonomy_key: str
                :param request_body: Request body of createMetadataTaxonomyLevel method
                :type request_body: List[MetadataTaxonomyLevel]
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
                        '/2.0/metadata_taxonomies/',
                        to_string(namespace),
                        '/',
                        to_string(taxonomy_key),
                        '/levels',
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
        return deserialize(response.data, MetadataTaxonomyLevels)

    def update_metadata_taxonomy_level_by_id(
        self,
        namespace: str,
        taxonomy_key: str,
        level_index: int,
        display_name: str,
        *,
        description: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> MetadataTaxonomyLevel:
        """
                Updates an existing metadata taxonomy level.
                :param namespace: The namespace of the metadata taxonomy.
        Example: "enterprise_123456"
                :type namespace: str
                :param taxonomy_key: The key of the metadata taxonomy.
        Example: "geography"
                :type taxonomy_key: str
                :param level_index: The index of the metadata taxonomy level.
        Example: 1
                :type level_index: int
                :param display_name: The display name of the taxonomy level.
                :type display_name: str
                :param description: The description of the taxonomy level., defaults to None
                :type description: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'displayName': display_name, 'description': description}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/metadata_taxonomies/',
                        to_string(namespace),
                        '/',
                        to_string(taxonomy_key),
                        '/levels/',
                        to_string(level_index),
                    ]
                ),
                method='PATCH',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, MetadataTaxonomyLevel)

    def add_metadata_taxonomy_level(
        self,
        namespace: str,
        taxonomy_key: str,
        display_name: str,
        *,
        description: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> MetadataTaxonomyLevels:
        """
                Creates a new metadata taxonomy level and appends it to the existing levels.

                If there are no levels defined yet, this will create the first level.

                :param namespace: The namespace of the metadata taxonomy.
        Example: "enterprise_123456"
                :type namespace: str
                :param taxonomy_key: The key of the metadata taxonomy.
        Example: "geography"
                :type taxonomy_key: str
                :param display_name: The display name of the taxonomy level.
                :type display_name: str
                :param description: The description of the taxonomy level., defaults to None
                :type description: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'displayName': display_name, 'description': description}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/metadata_taxonomies/',
                        to_string(namespace),
                        '/',
                        to_string(taxonomy_key),
                        '/levels:append',
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
        return deserialize(response.data, MetadataTaxonomyLevels)

    def delete_metadata_taxonomy_level(
        self,
        namespace: str,
        taxonomy_key: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> MetadataTaxonomyLevels:
        """
                Deletes the last level of the metadata taxonomy.
                :param namespace: The namespace of the metadata taxonomy.
        Example: "enterprise_123456"
                :type namespace: str
                :param taxonomy_key: The key of the metadata taxonomy.
        Example: "geography"
                :type taxonomy_key: str
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
                        '/2.0/metadata_taxonomies/',
                        to_string(namespace),
                        '/',
                        to_string(taxonomy_key),
                        '/levels:trim',
                    ]
                ),
                method='POST',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, MetadataTaxonomyLevels)

    def get_metadata_taxonomy_nodes(
        self,
        namespace: str,
        taxonomy_key: str,
        *,
        level: Optional[List[int]] = None,
        parent: Optional[List[str]] = None,
        ancestor: Optional[List[str]] = None,
        query: Optional[str] = None,
        include_total_result_count: Optional[bool] = None,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> MetadataTaxonomyNodes:
        """
                Used to retrieve metadata taxonomy nodes based on the parameters specified.

                Results are sorted in lexicographic order unless a `query` parameter is passed.


                With a `query` parameter specified, results are sorted in order of relevance.

                :param namespace: The namespace of the metadata taxonomy.
        Example: "enterprise_123456"
                :type namespace: str
                :param taxonomy_key: The key of the metadata taxonomy.
        Example: "geography"
                :type taxonomy_key: str
                :param level: Filters results by taxonomy level. Multiple values can be provided.
        Results include nodes that match any of the specified values., defaults to None
                :type level: Optional[List[int]], optional
                :param parent: Node identifier of a direct parent node. Multiple values can be provided.
        Results include nodes that match any of the specified values., defaults to None
                :type parent: Optional[List[str]], optional
                :param ancestor: Node identifier of any ancestor node. Multiple values can be provided.
        Results include nodes that match any of the specified values., defaults to None
                :type ancestor: Optional[List[str]], optional
                :param query: Query text to search for the taxonomy nodes., defaults to None
                :type query: Optional[str], optional
                :param include_total_result_count: When set to `true` this provides the total number of nodes that matched the query.
        The response will compute counts of up to 10,000 elements. Defaults to `false`., defaults to None
                :type include_total_result_count: Optional[bool], optional
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'level': to_string(level),
                'parent': to_string(parent),
                'ancestor': to_string(ancestor),
                'query': to_string(query),
                'include-total-result-count': to_string(include_total_result_count),
                'marker': to_string(marker),
                'limit': to_string(limit),
            }
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/metadata_taxonomies/',
                        to_string(namespace),
                        '/',
                        to_string(taxonomy_key),
                        '/nodes',
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
        return deserialize(response.data, MetadataTaxonomyNodes)

    def create_metadata_taxonomy_node(
        self,
        namespace: str,
        taxonomy_key: str,
        display_name: str,
        level: int,
        *,
        parent_id: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> MetadataTaxonomyNode:
        """
                Creates a new metadata taxonomy node.
                :param namespace: The namespace of the metadata taxonomy.
        Example: "enterprise_123456"
                :type namespace: str
                :param taxonomy_key: The key of the metadata taxonomy.
        Example: "geography"
                :type taxonomy_key: str
                :param display_name: The display name of the taxonomy node.
                :type display_name: str
                :param level: The level of the taxonomy node.
                :type level: int
                :param parent_id: The identifier of the parent taxonomy node.
        Omit this field for root-level nodes., defaults to None
                :type parent_id: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'displayName': display_name,
            'level': level,
            'parentId': parent_id,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/metadata_taxonomies/',
                        to_string(namespace),
                        '/',
                        to_string(taxonomy_key),
                        '/nodes',
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
        return deserialize(response.data, MetadataTaxonomyNode)

    def get_metadata_taxonomy_node_by_id(
        self,
        namespace: str,
        taxonomy_key: str,
        node_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> MetadataTaxonomyNode:
        """
                Retrieves a metadata taxonomy node by its identifier.
                :param namespace: The namespace of the metadata taxonomy.
        Example: "enterprise_123456"
                :type namespace: str
                :param taxonomy_key: The key of the metadata taxonomy.
        Example: "geography"
                :type taxonomy_key: str
                :param node_id: The identifier of the metadata taxonomy node.
        Example: "14d3d433-c77f-49c5-b146-9dea370f6e32"
                :type node_id: str
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
                        '/2.0/metadata_taxonomies/',
                        to_string(namespace),
                        '/',
                        to_string(taxonomy_key),
                        '/nodes/',
                        to_string(node_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, MetadataTaxonomyNode)

    def update_metadata_taxonomy_node(
        self,
        namespace: str,
        taxonomy_key: str,
        node_id: str,
        *,
        display_name: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> MetadataTaxonomyNode:
        """
                Updates an existing metadata taxonomy node.
                :param namespace: The namespace of the metadata taxonomy.
        Example: "enterprise_123456"
                :type namespace: str
                :param taxonomy_key: The key of the metadata taxonomy.
        Example: "geography"
                :type taxonomy_key: str
                :param node_id: The identifier of the metadata taxonomy node.
        Example: "14d3d433-c77f-49c5-b146-9dea370f6e32"
                :type node_id: str
                :param display_name: The display name of the taxonomy node., defaults to None
                :type display_name: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'displayName': display_name}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/metadata_taxonomies/',
                        to_string(namespace),
                        '/',
                        to_string(taxonomy_key),
                        '/nodes/',
                        to_string(node_id),
                    ]
                ),
                method='PATCH',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, MetadataTaxonomyNode)

    def delete_metadata_taxonomy_node(
        self,
        namespace: str,
        taxonomy_key: str,
        node_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Delete a metadata taxonomy node.

                This deletion is permanent and cannot be reverted.


                Only metadata taxonomy nodes without any children can be deleted.

                :param namespace: The namespace of the metadata taxonomy.
        Example: "enterprise_123456"
                :type namespace: str
                :param taxonomy_key: The key of the metadata taxonomy.
        Example: "geography"
                :type taxonomy_key: str
                :param node_id: The identifier of the metadata taxonomy node.
        Example: "14d3d433-c77f-49c5-b146-9dea370f6e32"
                :type node_id: str
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
                        '/2.0/metadata_taxonomies/',
                        to_string(namespace),
                        '/',
                        to_string(taxonomy_key),
                        '/nodes/',
                        to_string(node_id),
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

    def get_metadata_template_field_options(
        self,
        namespace: str,
        template_key: str,
        field_key: str,
        *,
        level: Optional[List[int]] = None,
        parent: Optional[List[str]] = None,
        ancestor: Optional[List[str]] = None,
        query: Optional[str] = None,
        include_total_result_count: Optional[bool] = None,
        only_selectable_options: Optional[bool] = None,
        marker: Optional[str] = None,
        limit: Optional[int] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> MetadataTaxonomyNodes:
        """
                Used to retrieve metadata taxonomy nodes which are available for the taxonomy field based

                on its configuration and the parameters specified.


                Results are sorted in lexicographic order unless a `query` parameter is passed.


                With a `query` parameter specified, results are sorted in order of relevance.

                :param namespace: The namespace of the metadata taxonomy.
        Example: "enterprise_123456"
                :type namespace: str
                :param template_key: The name of the metadata template.
        Example: "properties"
                :type template_key: str
                :param field_key: The key of the metadata taxonomy field in the template.
        Example: "geography"
                :type field_key: str
                :param level: Filters results by taxonomy level. Multiple values can be provided.
        Results include nodes that match any of the specified values., defaults to None
                :type level: Optional[List[int]], optional
                :param parent: Node identifier of a direct parent node. Multiple values can be provided.
        Results include nodes that match any of the specified values., defaults to None
                :type parent: Optional[List[str]], optional
                :param ancestor: Node identifier of any ancestor node. Multiple values can be provided.
        Results include nodes that match any of the specified values., defaults to None
                :type ancestor: Optional[List[str]], optional
                :param query: Query text to search for the taxonomy nodes., defaults to None
                :type query: Optional[str], optional
                :param include_total_result_count: When set to `true` this provides the total number of nodes that matched the query.
        The response will compute counts of up to 10,000 elements. Defaults to `false`., defaults to None
                :type include_total_result_count: Optional[bool], optional
                :param only_selectable_options: When set to `true`, this only returns valid selectable options for this template
        taxonomy field. Otherwise, it returns all taxonomy nodes, whether or not they are selectable.
        Defaults to `true`., defaults to None
                :type only_selectable_options: Optional[bool], optional
                :param marker: Defines the position marker at which to begin returning results. This is
        used when paginating using marker-based pagination.

        This requires `usemarker` to be set to `true`., defaults to None
                :type marker: Optional[str], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {
                'level': to_string(level),
                'parent': to_string(parent),
                'ancestor': to_string(ancestor),
                'query': to_string(query),
                'include-total-result-count': to_string(include_total_result_count),
                'only-selectable-options': to_string(only_selectable_options),
                'marker': to_string(marker),
                'limit': to_string(limit),
            }
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/metadata_templates/',
                        to_string(namespace),
                        '/',
                        to_string(template_key),
                        '/fields/',
                        to_string(field_key),
                        '/options',
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
        return deserialize(response.data, MetadataTaxonomyNodes)
