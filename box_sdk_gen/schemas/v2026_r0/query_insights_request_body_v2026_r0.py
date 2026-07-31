from typing import Optional

from typing import Dict

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.query_ancestor_reference_v2026_r0 import (
    QueryAncestorReferenceV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.query_insights_group_by_v2026_r0 import (
    QueryInsightsGroupByV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.query_insights_metric_definition_v2026_r0 import (
    QueryInsightsMetricDefinitionV2026R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class QueryInsightsRequestBodyV2026R0QueryField(BaseObject):
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


class QueryInsightsRequestBodyV2026R0(BaseObject):
    def __init__(
        self,
        query: QueryInsightsRequestBodyV2026R0QueryField,
        metrics: Dict[str, QueryInsightsMetricDefinitionV2026R0],
        **kwargs
    ):
        """
                :param query: The filtering and grouping definition. Filters are applied first, followed
        by grouping, before metrics are computed.
                :type query: QueryInsightsRequestBodyV2026R0QueryField
                :param metrics: A map of user-defined metric aliases to their definitions. A maximum of 10
        metrics may be defined. Each alias must be a unique, non-empty string of up
        to 256 characters, containing only letters, digits, `_`, `-`, or `.`, and
        must not start with a digit, `_`, `-`, or `.`. May be empty to request
        only a total count.
                :type metrics: Dict[str, QueryInsightsMetricDefinitionV2026R0]
        """
        super().__init__(**kwargs)
        self.query = query
        self.metrics = metrics
