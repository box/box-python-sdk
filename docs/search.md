# SearchManager

- [Query files/folders by metadata](#query-files-folders-by-metadata)
- [Search for content](#search-for-content)

## Query files/folders by metadata

Create a search using SQL-like syntax to return items that match specific
metadata.

By default, this endpoint returns only the most basic info about the items for
which the query matches. To get additional fields for each item, including any
of the metadata, use the `fields` attribute in the query.

This operation is performed by calling function `search_by_metadata_query`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-metadata-queries-execute-read/).

<!-- sample post_metadata_queries_execute_read -->

```python
client.search.search_by_metadata_query(
    search_from,
    "0",
    query="name = :name AND age < :age AND birthDate >= :birthDate AND countryCode = :countryCode AND sports = :sports",
    query_params={
        "name": "John",
        "age": 50,
        "birthDate": "2001-01-01T02:20:10.120Z",
        "countryCode": "US",
        "sports": ["basketball", "tennis"],
    },
)
```

### Arguments

- from\_ `str`
  - Specifies the template used in the query. Must be in the form `scope.templateKey`. Not all templates can be used in this field, most notably the built-in, Box-provided classification templates can not be used in a query.
- query `Optional[str]`
  - The query to perform. A query is a logical expression that is very similar to a SQL `SELECT` statement. Values in the search query can be turned into parameters specified in the `query_param` arguments list to prevent having to manually insert search values into the query string. For example, a value of `:amount` would represent the `amount` value in `query_params` object.
- query_params `Optional[Dict]`
  - Set of arguments corresponding to the parameters specified in the `query`. The type of each parameter used in the `query_params` must match the type of the corresponding metadata template field.
- ancestor_folder_id `str`
  - The ID of the folder that you are restricting the query to. A value of zero will return results from all folders you have access to. A non-zero value will only return results found in the folder corresponding to the ID or in any of its subfolders.
- order_by `Optional[List[SearchByMetadataQueryOrderBy]]`
  - A list of template fields and directions to sort the metadata query results by. The ordering `direction` must be the same for each item in the array.
- limit `Optional[int]`
  - A value between 0 and 100 that indicates the maximum number of results to return for a single request. This only specifies a maximum boundary and will not guarantee the minimum number of results returned.
- marker `Optional[str]`
  - Marker to use for requesting the next page.
- fields `Optional[List[str]]`
  - By default, this endpoint returns only the most basic info about the items for which the query matches. This attribute can be used to specify a list of additional attributes to return for any item, including its metadata. This attribute takes a list of item fields, metadata template identifiers, or metadata template field identifiers. For example: _ `created_by` will add the details of the user who created the item to the response. _ `metadata.<scope>.<templateKey>` will return the mini-representation of the metadata instance identified by the `scope` and `templateKey`. \* `metadata.<scope>.<templateKey>.<field>` will return all the mini-representation of the metadata instance identified by the `scope` and `templateKey` plus the field specified by the `field` name. Multiple fields for the same `scope` and `templateKey` can be defined.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataQueryResults`.

Returns a list of files and folders that match this metadata query.

## Search for content

Searches for files, folders, web links, and shared files across the
users content or across the entire enterprise.

This operation is performed by calling function `search_for_content`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-search/).

<!-- sample get_search -->

```python
client.search.search_for_content(
    ancestor_folder_ids=["0"],
    mdfilters=[
        MetadataFilter(
            filters=search_filters,
            scope=MetadataFilterScopeField.ENTERPRISE,
            template_key=template_key,
        )
    ],
)
```

### Arguments

- query `Optional[str]`
  - The string to search for. This query is matched against item names, descriptions, text content of files, and various other fields of the different item types. This parameter supports a variety of operators to further refine the results returns. _ `""` - by wrapping a query in double quotes only exact matches are returned by the API. Exact searches do not return search matches based on specific character sequences. Instead, they return matches based on phrases, that is, word sequences. For example: A search for `"Blue-Box"` may return search results including the sequence `"blue.box"`, `"Blue Box"`, and `"Blue-Box"`; any item containing the words `Blue` and `Box` consecutively, in the order specified. _ `AND` - returns items that contain both the search terms. For example, a search for `marketing AND BoxWorks` returns items that have both `marketing` and `BoxWorks` within its text in any order. It does not return a result that only has `BoxWorks` in its text. _ `OR` - returns items that contain either of the search terms. For example, a search for `marketing OR BoxWorks` returns a result that has either `marketing` or `BoxWorks` within its text. Using this operator is not necessary as we implicitly interpret multi-word queries as `OR` unless another supported boolean term is used. _ `NOT` - returns items that do not contain the search term provided. For example, a search for `marketing AND NOT BoxWorks` returns a result that has only `marketing` within its text. Results containing `BoxWorks` are omitted. We do not support lower case (that is, `and`, `or`, and `not`) or mixed case (that is, `And`, `Or`, and `Not`) operators. This field is required unless the `mdfilters` parameter is defined.
- scope `Optional[SearchForContentScope]`
  - Limits the search results to either the files that the user has access to, or to files available to the entire enterprise. The scope defaults to `user_content`, which limits the search results to content that is available to the currently authenticated user. The `enterprise_content` can be requested by an admin through our support channels. Once this scope has been enabled for a user, it will allow that use to query for content across the entire enterprise and not only the content that they have access to.
- file_extensions `Optional[List[str]]`
  - Limits the search results to any files that match any of the provided file extensions. This list is a comma-separated list of file extensions without the dots.
- created_at_range `Optional[List[str]]`
  - Limits the search results to any items created within a given date range. Date ranges are defined as comma separated RFC3339 timestamps. If the start date is omitted (`,2014-05-17T13:35:01-07:00`) anything created before the end date will be returned. If the end date is omitted (`2014-05-15T13:35:01-07:00,`) the current date will be used as the end date instead.
- updated_at_range `Optional[List[str]]`
  - Limits the search results to any items updated within a given date range. Date ranges are defined as comma separated RFC3339 timestamps. If the start date is omitted (`,2014-05-17T13:35:01-07:00`) anything updated before the end date will be returned. If the end date is omitted (`2014-05-15T13:35:01-07:00,`) the current date will be used as the end date instead.
- size_range `Optional[List[int]]`
  - Limits the search results to any items with a size within a given file size range. This applied to files and folders. Size ranges are defined as comma separated list of a lower and upper byte size limit (inclusive). The upper and lower bound can be omitted to create open ranges.
- owner_user_ids `Optional[List[str]]`
  - Limits the search results to any items that are owned by the given list of owners, defined as a list of comma separated user IDs. The items still need to be owned or shared with the currently authenticated user for them to show up in the search results. If the user does not have access to any files owned by any of the users an empty result set will be returned. To search across an entire enterprise, we recommend using the `enterprise_content` scope parameter which can be requested with our support team.
- recent_updater_user_ids `Optional[List[str]]`
  - Limits the search results to any items that have been updated by the given list of users, defined as a list of comma separated user IDs. The items still need to be owned or shared with the currently authenticated user for them to show up in the search results. If the user does not have access to any files owned by any of the users an empty result set will be returned. This feature only searches back to the last 10 versions of an item.
- ancestor_folder_ids `Optional[List[str]]`
  - Limits the search results to items within the given list of folders, defined as a comma separated lists of folder IDs. Search results will also include items within any subfolders of those ancestor folders. The folders still need to be owned or shared with the currently authenticated user. If the folder is not accessible by this user, or it does not exist, a `HTTP 404` error code will be returned instead. To search across an entire enterprise, we recommend using the `enterprise_content` scope parameter which can be requested with our support team.
- content_types `Optional[List[SearchForContentContentTypes]]`
  - Limits the search results to any items that match the search query for a specific part of the file, for example the file description. Content types are defined as a comma separated lists of Box recognized content types. The allowed content types are as follows. _ `name` - The name of the item, as defined by its `name` field. _ `description` - The description of the item, as defined by its `description` field. _ `file_content` - The actual content of the file. _ `comments` - The content of any of the comments on a file or folder. \* `tags` - Any tags that are applied to an item, as defined by its `tags` field.
- type `Optional[SearchForContentType]`
  - Limits the search results to any items of this type. This parameter only takes one value. By default the API returns items that match any of these types. _ `file` - Limits the search results to files, _ `folder` - Limits the search results to folders, \* `web_link` - Limits the search results to web links, also known as bookmarks.
- trash_content `Optional[SearchForContentTrashContent]`
  - Determines if the search should look in the trash for items. By default, this API only returns search results for items not currently in the trash (`non_trashed_only`). _ `trashed_only` - Only searches for items currently in the trash _ `non_trashed_only` - Only searches for items currently not in the trash \* `all_items` - Searches for both trashed and non-trashed items.
- mdfilters `Optional[List[MetadataFilter]]`
  - Limits the search results to any items for which the metadata matches the provided filter. This parameter is a list that specifies exactly **one** metadata template used to filter the search results. The parameter is required unless the `query` parameter is provided.
- sort `Optional[SearchForContentSort]`
  - Defines the order in which search results are returned. This API defaults to returning items by relevance unless this parameter is explicitly specified. _ `relevance` (default) returns the results sorted by relevance to the query search term. The relevance is based on the occurrence of the search term in the items name, description, content, and additional properties. _ `modified_at` returns the results ordered in descending order by date at which the item was last modified.
- direction `Optional[SearchForContentDirection]`
  - Defines the direction in which search results are ordered. This API defaults to returning items in descending (`DESC`) order unless this parameter is explicitly specified. When results are sorted by `relevance` the ordering is locked to returning items in descending order of relevance, and this parameter is ignored.
- limit `Optional[int]`
  - Defines the maximum number of items to return as part of a page of results.
- include_recent_shared_links `Optional[bool]`
  - Defines whether the search results should include any items that the user recently accessed through a shared link. When this parameter has been set to true, the format of the response of this API changes to return a list of [Search Results with Shared Links](r://search_results_with_shared_links).
- fields `Optional[List[str]]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response. Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- offset `Optional[int]`
  - The offset of the item at which to begin the response. Queries with offset parameter value exceeding 10000 will be rejected with a 400 response.
- deleted_user_ids `Optional[List[str]]`
  - Limits the search results to items that were deleted by the given list of users, defined as a list of comma separated user IDs. The `trash_content` parameter needs to be set to `trashed_only`. If searching in trash is not performed, an empty result set is returned. The items need to be owned or shared with the currently authenticated user for them to show up in the search results. If the user does not have access to any files owned by any of the users, an empty result set is returned. Data available from 2023-02-01 onwards.
- deleted_at_range `Optional[List[str]]`
  - Limits the search results to any items deleted within a given date range. Date ranges are defined as comma separated RFC3339 timestamps. If the start date is omitted (`2014-05-17T13:35:01-07:00`), anything deleted before the end date will be returned. If the end date is omitted (`2014-05-15T13:35:01-07:00`), the current date will be used as the end date instead. The `trash_content` parameter needs to be set to `trashed_only`. If searching in trash is not performed, then an empty result is returned. Data available from 2023-02-01 onwards.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `SearchResultsResponse`.

Returns a collection of search results. If there are no matching
search results, the `entries` array will be empty.
