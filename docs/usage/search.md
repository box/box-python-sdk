Search
======

Search provides a powerful way of finding items that are accessible by a single user or an entire 
enterprise.

- [Search for Content](#search-for-content)
- [Metadata Query](#metadata-query)

Search for Content
------------------

To get a list of items matching a search query, call [`search.query(query, limit=None, offset=0, ancestor_folders=None, file_extensions=None, metadata_filters=None, result_type=None, content_types=None, scope=None, created_at_range=None, updated_at_range=None, size_range=None, owner_users=None, trash_content=None, fields=None, sort=None, direction=None, **kwargs)`][query] will return an `Iterable` that allows you
to iterate over the [`Item`][item_class] objects in the collection.

<!-- sample get_search -->
```python
items = client.search().query(query='TEST QUERY', limit=100, file_extensions=['pdf', 'doc'])
for item in items:
    print(f'The item ID is {item.id} and the item name is {item.name}')
```

[query]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.search.Search.query
[item_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item

### Metadata Search

To filter by metadata in your search, first create [`MetadataSearchFilter`][metadata_search_filter] object with the 
specified `template_key` and `scope` as well as adding filter, `field_key` and `value` with 
[`metadata_filter.add_value_based_filter(field_key, value)`][add_value_based_filter]. Next, create a 
[`MetadataSearchFilters`][metadata_search_filters] object and call [`metadata_filters.add_filter(metadata_filter)`][add_filter] 
and pass in the [`MetadataSearchFilter`][metadata_search_filter] object created earlier. Finally, call 
[`search.query(query, metadata_filters=None, **kwargs)`][query] with [`MetadataSearchFilters`][metadata_search_filters] 
object passed in.

```python
from boxsdk.object.search import MetadataSearchFilter, MetadataSearchFilters

metadata_search_filter = MetadataSearchFilter(template_key='marketingCollateral', scope='enterprise')
metadata_search_filter.add_value_based_filter(field_key='documentType', value='datasheet')
metadata_search_filter.add_value_based_filter(field_key='clientNumber', value='a123')
metadata_search_filters = MetadataSearchFilters()
metadata_search_filters.add_filter(metadata_search_filter)

client.search().query(None, limit=100, offset=0, metadata_filters=metadata_search_filters)
```

[metadata_search_filter]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.search.MetadataSearchFilter
[metadata_search_filters]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.search.MetadataSearchFilters
[add_value_based_filter]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.search.MetadataSearchFilter.add_value_based_filter
[add_filter]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.search.MetadataSearchFilters.add_filter

### Search with Shared Link Items

To get a list of items matching a search query, including items that a user might have accessed recently through a shared link, call [`search.query_with_shared_links(query, limit=None, offset=0, ancestor_folders=None, file_extensions=None, metadata_filters=None, result_type=None, content_types=None, scope=None, created_at_range=None, updated_at_range=None, size_range=None, owner_users=None, trash_content=None, fields=None, sort=None, direction=None, **kwargs)`][query_with_shared_links]. This method will return an `Iterable` that allows you
to iterate over the search result objects in the collection.

<!-- sample get_search_with_shared_links -->
```python
search_results = client.search().query_with_shared_links(query='TEST QUERY', limit=100, file_extensions=['pdf', 'doc'])
for search_result in search_results:
    print(f'The item ID is {search_result.item.id} and the item name is {search_result.item.name}')
```

[query_with_shared_links]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.search.Search.query_with_shared_links

Metadata Query
--------------
To search using SQL-like syntax to return items that match specific metadata, call `search.metadata_query(from_template, ancestor_folder_id, query=None, query_params=None, use_index=None, order_by=None, marker=None, limit=None, fields=None)` 

**Note:** paramter `use_index` is deprecated and if provided, will be ignored. The current way to create an index is to contact the MDQ team directly via email. MDQ will now use static query analysis to use the index that is most efficient for the call.



By default, this method returns only the most basic info about the items for which the query matches. To get additional fields for each item, including any of the metadata, use the fields parameter.

```python
from_template = 'enterprise_12345.someTemplate'
ancestor_folder_id = '5555'
query = 'amount >= :arg'
query_params = {'arg': 100}
order_by = [
    {
        'field_key': 'amount',
        'direction': 'asc'
    }
]
fields = ['type', 'id', 'name', 'metadata.enterprise_67890.catalogImages.$parent']
limit = 2
marker = 'AAAAAmVYB1FWec8GH6yWu2nwmanfMh07IyYInaa7DZDYjgO1H4KoLW29vPlLY173OKs'
items = client.search().metadata_query(
    from_template=from_template,
    ancestor_folder_id=ancestor_folder_id,
    query=query,
    query_params=query_params,
    order_by=order_by,
    marker=marker,
    limit=limit,
    fields=fields
    )
for item in items:
    print(f'The item ID is {item.id} and the item name is {item.name}')
```
