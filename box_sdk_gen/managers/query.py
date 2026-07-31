from typing import Optional

from typing import Dict

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.schemas.v2026_r0.query_ancestor_reference_v2026_r0 import (
    QueryAncestorReferenceV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.query_insights_group_by_v2026_r0 import (
    QueryInsightsGroupByV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.query_order_by_v2026_r0 import QueryOrderByV2026R0

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.v2026_r0.query_insights_metric_definition_v2026_r0 import (
    QueryInsightsMetricDefinitionV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.query_results_v2026_r0 import QueryResultsV2026R0

from box_sdk_gen.schemas.v2026_r0.client_error_v2026_r0 import ClientErrorV2026R0

from box_sdk_gen.parameters.v2026_r0.box_version_header_v2026_r0 import (
    BoxVersionHeaderV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.query_request_body_v2026_r0 import (
    QueryRequestBodyV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.query_insights_v2026_r0 import QueryInsightsV2026R0

from box_sdk_gen.schemas.v2026_r0.query_insights_request_body_v2026_r0 import (
    QueryInsightsRequestBodyV2026R0,
)

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


class CreateQueryV2026R0Query(BaseObject):
    def __init__(
        self,
        predicate: str,
        *,
        params: Optional[Dict] = None,
        ancestors: Optional[List[QueryAncestorReferenceV2026R0]] = None,
        **kwargs
    ):
        """
                :param predicate: A logical expression used to filter the dataset, similar to an SQL
        `WHERE` clause. May include named parameters referenced as
        `:placeholder`.
                :type predicate: str
                :param params: A map of placeholder names (without the `:` prefix) to their values.
        Required only when the predicate contains parameter placeholders. The
        type of each value must match the type of the field it is compared to., defaults to None
                :type params: Optional[Dict], optional
                :param ancestors: Restricts results to the specified ancestor entities and their
        recursive descendants. The user must have read access to every listed
        ancestor., defaults to None
                :type ancestors: Optional[List[QueryAncestorReferenceV2026R0]], optional
        """
        super().__init__(**kwargs)
        self.predicate = predicate
        self.params = params
        self.ancestors = ancestors


class CreateQueryInsightV2026R0Query(BaseObject):
    def __init__(
        self,
        predicate: str,
        *,
        params: Optional[Dict] = None,
        ancestors: Optional[List[QueryAncestorReferenceV2026R0]] = None,
        group_by: Optional[List[QueryInsightsGroupByV2026R0]] = None,
        **kwargs
    ):
        """
                :param predicate: A logical expression used to filter the dataset prior to metric
        computation, similar to an SQL `WHERE` clause. May include
        named parameters referenced as `:placeholder`.
                :type predicate: str
                :param params: A map of placeholder names (without the `:` prefix) to their values.
        Required only when the predicate contains parameter placeholders. The
        type of each value must match the type of the field it is compared to., defaults to None
                :type params: Optional[Dict], optional
                :param ancestors: Restricts results to items contained within any of the specified
        ancestors. The user must have access to every listed ancestor. When
        omitted, insights are computed across all accessible items., defaults to None
                :type ancestors: Optional[List[QueryAncestorReferenceV2026R0]], optional
                :param group_by: Defines how data is grouped for insights computation. Currently only a
        single grouping field is supported., defaults to None
                :type group_by: Optional[List[QueryInsightsGroupByV2026R0]], optional
        """
        super().__init__(**kwargs)
        self.predicate = predicate
        self.params = params
        self.ancestors = ancestors
        self.group_by = group_by


class QueryManager:
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

    def create_query_v2026_r0(
        self,
        query: CreateQueryV2026R0Query,
        *,
        order_by: Optional[List[QueryOrderByV2026R0]] = None,
        limit: Optional[int] = None,
        fields: Optional[List[str]] = None,
        marker: Optional[str] = None,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> QueryResultsV2026R0:
        """
                Runs a query to discover Box items using a logical predicate that can filter

                across item fields and metadata templates. Results can be sorted, paginated,


                and shaped to include additional item or metadata fields.

                :param query: The query definition, including the filtering predicate and its optional
        parameters and ancestor restrictions.
                :type query: CreateQueryV2026R0Query
                :param order_by: The sorting criteria for the result set. Entries are applied sequentially
        to define multi-level sorting., defaults to None
                :type order_by: Optional[List[QueryOrderByV2026R0]], optional
                :param limit: The maximum number of results to return. Defaults to `50` when not
        provided., defaults to None
                :type limit: Optional[int], optional
                :param fields: Controls which additional fields are included in each result entry. Each
        value must be one of: a fully qualified item field key (for example
        `box:item:name`), a metadata template key to hydrate the full template (for
        example `enterprise_12345678:project`), or a specific metadata template
        field key to hydrate a single field from the template (for example
        `enterprise_12345678:project:name`). When omitted, entries include only the
        item type and identifier., defaults to None
                :type fields: Optional[List[str]], optional
                :param marker: An opaque token returned from a previous response, used to continue
        retrieval. When provided, all other request parameters must exactly match
        those of the original request., defaults to None
                :type marker: Optional[str], optional
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'query': query,
            'order_by': order_by,
            'limit': limit,
            'fields': fields,
            'marker': marker,
        }
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join([self.network_session.base_urls.base_url, '/2.0/query']),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, QueryResultsV2026R0)

    def create_query_insight_v2026_r0(
        self,
        query: CreateQueryInsightV2026R0Query,
        metrics: Dict[str, QueryInsightsMetricDefinitionV2026R0],
        *,
        box_version: BoxVersionHeaderV2026R0 = BoxVersionHeaderV2026R0._2026_0,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> QueryInsightsV2026R0:
        """
                Computes aggregated metrics over Box items matching a query predicate.

                Filters are applied first, followed by optional grouping, after which the


                requested metrics (such as `sum`, `avg`, `min`, `max`, and `count`) are


                computed for each resulting group or over the entire filtered dataset.

                :param query: The filtering and grouping definition. Filters are applied first, followed
        by grouping, before metrics are computed.
                :type query: CreateQueryInsightV2026R0Query
                :param metrics: A map of user-defined metric aliases to their definitions. A maximum of 10
        metrics may be defined. Each alias must be a unique, non-empty string of up
        to 256 characters, containing only letters, digits, `_`, `-`, or `.`, and
        must not start with a digit, `_`, `-`, or `.`. May be empty to request
        only a total count.
                :type metrics: Dict[str, QueryInsightsMetricDefinitionV2026R0]
                :param box_version: Version header., defaults to BoxVersionHeaderV2026R0._2026_0
                :type box_version: BoxVersionHeaderV2026R0, optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'query': query, 'metrics': metrics}
        headers_map: Dict[str, str] = prepare_params(
            {'box-version': to_string(box_version), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/query_insights']
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
        return deserialize(response.data, QueryInsightsV2026R0)
