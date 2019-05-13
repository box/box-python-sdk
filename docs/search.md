Search
======

The search endpoint provides a powerful way of finding items that are accessible by a single user or an entire 
enterprise. Leverage the parameters listed below to generate targeted advanced searches.

Search for Content
------------------

To get a list of items matching a serch query, call [`search.query(query, limit=None, offset=0, **kwargs)`][query] will return an `Iterable` that allows you 
to iterate over the [`Item`][item_class] objects in the collection.

<!-- sample get_search -->
```python
items = client.search().query(query='TEST QUERY', limit=100, file_extensions=['pdf', 'doc'])
for item in items:
    print('The item ID is {0} and the item name is {1}'.format(item.id, item.name))
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

client.search(None, limit=100, offset=0, metadata_filters=metadata_search_filters)
```

[metadata_search_filter]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.search.MetadataSearchFilter
[metadata_search_filters]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.search.MetadataSearchFilters
[add_value_based_filter]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.search.MetadataSearchFilter.add_value_based_filter
[add_filter]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.search.MetadataSearchFilters.add_filter
