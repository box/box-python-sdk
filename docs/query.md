# QueryManager

- [Query for Box items](#query-for-box-items)
- [Create insights for Box items](#create-insights-for-box-items)

## Query for Box items

Runs a query to discover Box items using a logical predicate that can filter
across item fields and metadata templates. Results can be sorted, paginated,
and shaped to include additional item or metadata fields.

This operation is performed by calling function `create_query_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/post-query/).

_Currently we don't have an example for calling `create_query_v2026_r0` in integration tests_

### Arguments

- query `CreateQueryV2026R0Query`
  - The query definition, including the filtering predicate and its optional parameters and ancestor restrictions.
- order_by `Optional[List[QueryOrderByV2026R0]]`
  - The sorting criteria for the result set. Entries are applied sequentially to define multi-level sorting.
- limit `Optional[int]`
  - The maximum number of results to return. Defaults to `50` when not provided.
- fields `Optional[List[str]]`
  - Controls which additional fields are included in each result entry. Each value must be one of: a fully qualified item field key (for example `box:item:name`), a metadata template key to hydrate the full template (for example `enterprise_12345678:project`), or a specific metadata template field key to hydrate a single field from the template (for example `enterprise_12345678:project:name`). When omitted, entries include only the item type and identifier.
- marker `Optional[str]`
  - An opaque token returned from a previous response, used to continue retrieval. When provided, all other request parameters must exactly match those of the original request.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `QueryResultsV2026R0`.

Returns a paginated list of items matching the query.

## Create insights for Box items

Computes aggregated metrics over Box items matching a query predicate.
Filters are applied first, followed by optional grouping, after which the
requested metrics (such as `sum`, `avg`, `min`, `max`, and `count`) are
computed for each resulting group or over the entire filtered dataset.

This operation is performed by calling function `create_query_insight_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/post-query-insights/).

_Currently we don't have an example for calling `create_query_insight_v2026_r0` in integration tests_

### Arguments

- query `CreateQueryInsightV2026R0Query`
  - The filtering and grouping definition. Filters are applied first, followed by grouping, before metrics are computed.
- metrics `Dict[str, QueryInsightsMetricDefinitionV2026R0]`
  - A map of user-defined metric aliases to their definitions. A maximum of 10 metrics may be defined. Each alias must be a unique, non-empty string of up to 256 characters, containing only letters, digits, `_`, `-`, or `.`, and must not start with a digit, `_`, `-`, or `.`. May be empty to request only a total count.
- box_version `BoxVersionHeaderV2026R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `QueryInsightsV2026R0`.

Returns the computed insight entries.
