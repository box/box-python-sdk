# QueryManager

- [Box Query](#box-query)
- [Create insights for Box items](#create-insights-for-box-items)

## Box Query

Runs a query to discover Box items using a logical predicate, similar to a SQL
WHERE clause. The predicate can filter across multiple metadata templates and
item fields in a single request. Results can be sorted, paginated with markers,
and shaped with fields so each entry includes additional item or metadata
attributes.

This is the item-retrieval endpoint in the Query API (version 2026.0). Unlike
the [Metadata Query API](https://developer.box.com/reference/post-metadata-queries-execute-read),
it is not limited to a single metadata template or to files and folders. For
totals and grouped metrics over the same predicates, use
[Query Insights](https://developer.box.com/reference/v2026.0/post-query-insights)
instead of paging through every matching item.

For predicate syntax, parameters, examples, pagination behavior, and error
codes, see the
[Box Query guide](https://developer.box.com/guides/query/box-query). For shared
response schemas, including Query results and result entries, see
[Query resources](https://developer.box.com/reference/v2026.0/query-resources).

This operation is performed by calling function `create_query_v2026_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2026.0/post-query/).

<!-- sample post_query_v2026.0 -->

```python
client.query.create_query_v2026_r0(CreateQueryV2026R0Query(predicate=predicate, params={'name': 'John', 'age': 50}, ancestors=[QueryAncestorReferenceV2026R0(id='0', type='folder')]), limit=10, fields=['box:item:name', search_from])
```

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

<!-- sample post_query_insights_v2026.0 -->

```python
client.query.create_query_insight_v2026_r0(CreateQueryInsightV2026R0Query(predicate=predicate, params={'minAmount': 0}, ancestors=[QueryAncestorReferenceV2026R0(id='0', type='folder')], group_by=[QueryInsightsGroupByV2026R0(field=''.join([md_prefix, '.category']), bucket_limit=5)]), metrics)
```

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
