# MetadataTaxonomiesManager

- [Create metadata taxonomy](#create-metadata-taxonomy)
- [Get metadata taxonomies for namespace](#get-metadata-taxonomies-for-namespace)
- [Get metadata taxonomy by taxonomy key](#get-metadata-taxonomy-by-taxonomy-key)
- [Update metadata taxonomy](#update-metadata-taxonomy)
- [Remove metadata taxonomy](#remove-metadata-taxonomy)
- [Create metadata taxonomy levels](#create-metadata-taxonomy-levels)
- [Update metadata taxonomy level](#update-metadata-taxonomy-level)
- [Add metadata taxonomy level](#add-metadata-taxonomy-level)
- [Delete metadata taxonomy level](#delete-metadata-taxonomy-level)
- [List metadata taxonomy nodes](#list-metadata-taxonomy-nodes)
- [Create metadata taxonomy node](#create-metadata-taxonomy-node)
- [Get metadata taxonomy node by ID](#get-metadata-taxonomy-node-by-id)
- [Update metadata taxonomy node](#update-metadata-taxonomy-node)
- [Remove metadata taxonomy node](#remove-metadata-taxonomy-node)
- [List metadata template's options for taxonomy field](#list-metadata-templates-options-for-taxonomy-field)

## Create metadata taxonomy

Creates a new metadata taxonomy that can be used in
metadata templates.

This operation is performed by calling function `create_metadata_taxonomy`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-metadata-taxonomies/).

<!-- sample post_metadata_taxonomies -->

```python
client.metadata_taxonomies.create_metadata_taxonomy(display_name, namespace, key=taxonomy_key)
```

### Arguments

- key `Optional[str]`
  - The taxonomy key. If it is not provided in the request body, it will be generated from the `displayName`. The `displayName` would be converted to lower case, and all spaces and non-alphanumeric characters replaced with underscores.
- display_name `str`
  - The display name of the taxonomy.
- namespace `str`
  - The namespace of the metadata taxonomy to create.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTaxonomy`.

The schema representing the metadata taxonomy created.

## Get metadata taxonomies for namespace

Used to retrieve all metadata taxonomies in a namespace.

This operation is performed by calling function `get_metadata_taxonomies`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-metadata-taxonomies-id/).

<!-- sample get_metadata_taxonomies_id -->

```python
client.metadata_taxonomies.get_metadata_taxonomies(namespace)
```

### Arguments

- namespace `str`
  - The namespace of the metadata taxonomy. Example: "enterprise_123456"
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTaxonomies`.

Returns all of the metadata taxonomies within a namespace
and their corresponding schema.

## Get metadata taxonomy by taxonomy key

Used to retrieve a metadata taxonomy by taxonomy key.

This operation is performed by calling function `get_metadata_taxonomy_by_key`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-metadata-taxonomies-id-id/).

<!-- sample get_metadata_taxonomies_id_id -->

```python
client.metadata_taxonomies.get_metadata_taxonomy_by_key(namespace, taxonomy_key)
```

### Arguments

- namespace `str`
  - The namespace of the metadata taxonomy. Example: "enterprise_123456"
- taxonomy_key `str`
  - The key of the metadata taxonomy. Example: "geography"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTaxonomy`.

Returns the metadata taxonomy identified by the taxonomy key.

## Update metadata taxonomy

Updates an existing metadata taxonomy.

This operation is performed by calling function `update_metadata_taxonomy`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/patch-metadata-taxonomies-id-id/).

<!-- sample patch_metadata_taxonomies_id_id -->

```python
client.metadata_taxonomies.update_metadata_taxonomy(namespace, taxonomy_key, updated_display_name)
```

### Arguments

- namespace `str`
  - The namespace of the metadata taxonomy. Example: "enterprise_123456"
- taxonomy_key `str`
  - The key of the metadata taxonomy. Example: "geography"
- display_name `str`
  - The display name of the taxonomy.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTaxonomy`.

The schema representing the updated metadata taxonomy.

## Remove metadata taxonomy

Delete a metadata taxonomy.
This deletion is permanent and cannot be reverted.

This operation is performed by calling function `delete_metadata_taxonomy`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-metadata-taxonomies-id-id/).

<!-- sample delete_metadata_taxonomies_id_id -->

```python
client.metadata_taxonomies.delete_metadata_taxonomy(namespace, taxonomy_key)
```

### Arguments

- namespace `str`
  - The namespace of the metadata taxonomy. Example: "enterprise_123456"
- taxonomy_key `str`
  - The key of the metadata taxonomy. Example: "geography"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the metadata taxonomy is successfully deleted.

## Create metadata taxonomy levels

Creates new metadata taxonomy levels.

This operation is performed by calling function `create_metadata_taxonomy_level`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-metadata-taxonomies-id-id-levels/).

<!-- sample post_metadata_taxonomies_id_id_levels -->

```python
client.metadata_taxonomies.create_metadata_taxonomy_level(namespace, taxonomy_key, [MetadataTaxonomyLevel(display_name='Continent', description='Continent Level'), MetadataTaxonomyLevel(display_name='Country', description='Country Level')])
```

### Arguments

- namespace `str`
  - The namespace of the metadata taxonomy. Example: "enterprise_123456"
- taxonomy_key `str`
  - The key of the metadata taxonomy. Example: "geography"
- request_body `List[MetadataTaxonomyLevel]`
  - Request body of createMetadataTaxonomyLevel method
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTaxonomyLevels`.

Returns an array of all taxonomy levels.

## Update metadata taxonomy level

Updates an existing metadata taxonomy level.

This operation is performed by calling function `patch_metadata_taxonomies_id_id_levels_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/patch-metadata-taxonomies-id-id-levels-id/).

_Currently we don't have an example for calling `patch_metadata_taxonomies_id_id_levels_id` in integration tests_

### Arguments

- namespace `str`
  - The namespace of the metadata taxonomy. Example: "enterprise_123456"
- taxonomy_key `str`
  - The key of the metadata taxonomy. Example: "geography"
- level_index `int`
  - The index of the metadata taxonomy level. Example: 1
- display_name `str`
  - The display name of the taxonomy level.
- description `Optional[str]`
  - The description of the taxonomy level.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTaxonomyLevel`.

The updated taxonomy level.

## Add metadata taxonomy level

Creates a new metadata taxonomy level and appends it to the existing levels.
If there are no levels defined yet, this will create the first level.

This operation is performed by calling function `add_metadata_taxonomy_level`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-metadata-taxonomies-id-id-levels:append/).

<!-- sample post_metadata_taxonomies_id_id_levels:append -->

```python
client.metadata_taxonomies.add_metadata_taxonomy_level(namespace, taxonomy_key, 'Region', description='Region Description')
```

### Arguments

- namespace `str`
  - The namespace of the metadata taxonomy. Example: "enterprise_123456"
- taxonomy_key `str`
  - The key of the metadata taxonomy. Example: "geography"
- display_name `str`
  - The display name of the taxonomy level.
- description `Optional[str]`
  - The description of the taxonomy level.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTaxonomyLevels`.

Returns an array of all taxonomy levels.

## Delete metadata taxonomy level

Deletes the last level of the metadata taxonomy.

This operation is performed by calling function `delete_metadata_taxonomy_level`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-metadata-taxonomies-id-id-levels:trim/).

<!-- sample post_metadata_taxonomies_id_id_levels:trim -->

```python
client.metadata_taxonomies.delete_metadata_taxonomy_level(namespace, taxonomy_key)
```

### Arguments

- namespace `str`
  - The namespace of the metadata taxonomy. Example: "enterprise_123456"
- taxonomy_key `str`
  - The key of the metadata taxonomy. Example: "geography"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTaxonomyLevels`.

Returns an array of all taxonomy levels.

## List metadata taxonomy nodes

Used to retrieve metadata taxonomy nodes based on the parameters specified.
Results are sorted in lexicographic order unless a `query` parameter is passed.
With a `query` parameter specified, results are sorted in order of relevance.

This operation is performed by calling function `get_metadata_taxonomy_nodes`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-metadata-taxonomies-id-id-nodes/).

<!-- sample get_metadata_taxonomies_id_id_nodes -->

```python
client.metadata_taxonomies.get_metadata_taxonomy_nodes(namespace, taxonomy_key)
```

### Arguments

- namespace `str`
  - The namespace of the metadata taxonomy. Example: "enterprise_123456"
- taxonomy_key `str`
  - The key of the metadata taxonomy. Example: "geography"
- level `Optional[List[int]]`
  - Filters results by taxonomy level. Multiple values can be provided. Results include nodes that match any of the specified values.
- parent `Optional[List[str]]`
  - Node identifier of a direct parent node. Multiple values can be provided. Results include nodes that match any of the specified values.
- ancestor `Optional[List[str]]`
  - Node identifier of any ancestor node. Multiple values can be provided. Results include nodes that match any of the specified values.
- query `Optional[str]`
  - Query text to search for the taxonomy nodes.
- include_total_result_count `Optional[bool]`
  - When set to `true` this provides the total number of nodes that matched the query. The response will compute counts of up to 10,000 elements. Defaults to `false`.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTaxonomyNodes`.

Returns a list of the taxonomy nodes that match the specified parameters.

## Create metadata taxonomy node

Creates a new metadata taxonomy node.

This operation is performed by calling function `create_metadata_taxonomy_node`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-metadata-taxonomies-id-id-nodes/).

<!-- sample post_metadata_taxonomies_id_id_nodes -->

```python
client.metadata_taxonomies.create_metadata_taxonomy_node(namespace, taxonomy_key, 'Europe', 1)
```

### Arguments

- namespace `str`
  - The namespace of the metadata taxonomy. Example: "enterprise_123456"
- taxonomy_key `str`
  - The key of the metadata taxonomy. Example: "geography"
- display_name `str`
  - The display name of the taxonomy node.
- level `int`
  - The level of the taxonomy node.
- parent_id `Optional[str]`
  - The identifier of the parent taxonomy node. Omit this field for root-level nodes.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTaxonomyNode`.

The schema representing the taxonomy node created.

## Get metadata taxonomy node by ID

Retrieves a metadata taxonomy node by its identifier.

This operation is performed by calling function `get_metadata_taxonomy_node_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-metadata-taxonomies-id-id-nodes-id/).

<!-- sample get_metadata_taxonomies_id_id_nodes_id -->

```python
client.metadata_taxonomies.get_metadata_taxonomy_node_by_id(namespace, taxonomy_key, country_node.id)
```

### Arguments

- namespace `str`
  - The namespace of the metadata taxonomy. Example: "enterprise_123456"
- taxonomy_key `str`
  - The key of the metadata taxonomy. Example: "geography"
- node_id `str`
  - The identifier of the metadata taxonomy node. Example: "14d3d433-c77f-49c5-b146-9dea370f6e32"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTaxonomyNode`.

Returns the metadata taxonomy node that matches the identifier.

## Update metadata taxonomy node

Updates an existing metadata taxonomy node.

This operation is performed by calling function `update_metadata_taxonomy_node`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/patch-metadata-taxonomies-id-id-nodes-id/).

<!-- sample patch_metadata_taxonomies_id_id_nodes_id -->

```python
client.metadata_taxonomies.update_metadata_taxonomy_node(namespace, taxonomy_key, country_node.id, display_name='Poland UPDATED')
```

### Arguments

- namespace `str`
  - The namespace of the metadata taxonomy. Example: "enterprise_123456"
- taxonomy_key `str`
  - The key of the metadata taxonomy. Example: "geography"
- node_id `str`
  - The identifier of the metadata taxonomy node. Example: "14d3d433-c77f-49c5-b146-9dea370f6e32"
- display_name `Optional[str]`
  - The display name of the taxonomy node.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTaxonomyNode`.

The schema representing the updated taxonomy node.

## Remove metadata taxonomy node

Delete a metadata taxonomy node.
This deletion is permanent and cannot be reverted.
Only metadata taxonomy nodes without any children can be deleted.

This operation is performed by calling function `delete_metadata_taxonomy_node`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-metadata-taxonomies-id-id-nodes-id/).

<!-- sample delete_metadata_taxonomies_id_id_nodes_id -->

```python
client.metadata_taxonomies.delete_metadata_taxonomy_node(namespace, taxonomy_key, country_node.id)
```

### Arguments

- namespace `str`
  - The namespace of the metadata taxonomy. Example: "enterprise_123456"
- taxonomy_key `str`
  - The key of the metadata taxonomy. Example: "geography"
- node_id `str`
  - The identifier of the metadata taxonomy node. Example: "14d3d433-c77f-49c5-b146-9dea370f6e32"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the metadata taxonomy node is successfully deleted.

## List metadata template's options for taxonomy field

Used to retrieve metadata taxonomy nodes which are available for the taxonomy field based
on its configuration and the parameters specified.
Results are sorted in lexicographic order unless a `query` parameter is passed.
With a `query` parameter specified, results are sorted in order of relevance.

This operation is performed by calling function `get_metadata_template_field_options`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-metadata-templates-id-id-fields-id-options/).

_Currently we don't have an example for calling `get_metadata_template_field_options` in integration tests_

### Arguments

- namespace `str`
  - The namespace of the metadata taxonomy. Example: "enterprise_123456"
- template_key `str`
  - The name of the metadata template. Example: "properties"
- field_key `str`
  - The key of the metadata taxonomy field in the template. Example: "geography"
- level `Optional[List[int]]`
  - Filters results by taxonomy level. Multiple values can be provided. Results include nodes that match any of the specified values.
- parent `Optional[List[str]]`
  - Node identifier of a direct parent node. Multiple values can be provided. Results include nodes that match any of the specified values.
- ancestor `Optional[List[str]]`
  - Node identifier of any ancestor node. Multiple values can be provided. Results include nodes that match any of the specified values.
- query `Optional[str]`
  - Query text to search for the taxonomy nodes.
- include_total_result_count `Optional[bool]`
  - When set to `true` this provides the total number of nodes that matched the query. The response will compute counts of up to 10,000 elements. Defaults to `false`.
- only_selectable_options `Optional[bool]`
  - When set to `true`, this only returns valid selectable options for this template taxonomy field. Otherwise, it returns all taxonomy nodes, whether or not they are selectable. Defaults to `true`.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTaxonomyNodes`.

Returns a list of the taxonomy nodes that match the specified parameters.
