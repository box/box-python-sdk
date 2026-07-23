from typing import Optional

from typing import Dict

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2026_r0.query_ancestor_reference_v2026_r0 import (
    QueryAncestorReferenceV2026R0,
)

from box_sdk_gen.schemas.v2026_r0.query_order_by_v2026_r0 import QueryOrderByV2026R0

from box_sdk_gen.box.errors import BoxSDKError


class QueryRequestBodyV2026R0QueryField(BaseObject):
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


class QueryRequestBodyV2026R0(BaseObject):
    def __init__(
        self,
        query: QueryRequestBodyV2026R0QueryField,
        *,
        order_by: Optional[List[QueryOrderByV2026R0]] = None,
        limit: Optional[int] = None,
        fields: Optional[List[str]] = None,
        marker: Optional[str] = None,
        **kwargs
    ):
        """
                :param query: The query definition, including the filtering predicate and its optional
        parameters and ancestor restrictions.
                :type query: QueryRequestBodyV2026R0QueryField
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
        """
        super().__init__(**kwargs)
        self.query = query
        self.order_by = order_by
        self.limit = limit
        self.fields = fields
        self.marker = marker
