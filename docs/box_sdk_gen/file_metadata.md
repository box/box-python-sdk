# FileMetadataManager

- [List metadata instances on file](#list-metadata-instances-on-file)
- [Get metadata instance on file](#get-metadata-instance-on-file)
- [Create metadata instance on file](#create-metadata-instance-on-file)
- [Update metadata instance on file](#update-metadata-instance-on-file)
- [Remove metadata instance from file](#remove-metadata-instance-from-file)

## List metadata instances on file

Retrieves all metadata for a given file.

This operation is performed by calling function `get_file_metadata`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-files-id-metadata/).

<!-- sample get_files_id_metadata -->

```python
client.file_metadata.get_file_metadata(file.id)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Metadatas`.

Returns all the metadata associated with a file.

This API does not support pagination and will therefore always return
all of the metadata associated to the file.

## Get metadata instance on file

Retrieves the instance of a metadata template that has been applied to a
file.

This operation is performed by calling function `get_file_metadata_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-files-id-metadata-id-id/).

<!-- sample get_files_id_metadata_id_id -->

```python
client.file_metadata.get_file_metadata_by_id(file.id, GetFileMetadataByIdScope.GLOBAL, 'properties')
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- scope `GetFileMetadataByIdScope`
  - The scope of the metadata template. Example: "global"
- template_key `str`
  - The name of the metadata template. Example: "properties"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataFull`.

An instance of the metadata template that includes
additional "key:value" pairs defined by the user or
an application.

## Create metadata instance on file

Applies an instance of a metadata template to a file.

In most cases only values that are present in the metadata template
will be accepted, except for the `global.properties` template which accepts
any key-value pair.

This operation is performed by calling function `create_file_metadata_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-files-id-metadata-id-id/).

<!-- sample post_files_id_metadata_id_id -->

```python
client.file_metadata.create_file_metadata_by_id(file.id, CreateFileMetadataByIdScope.ENTERPRISE, template_key, {'name': 'John', 'age': 23, 'birthDate': '2001-01-03T02:20:50.520Z', 'countryCode': 'US', 'sports': ['basketball', 'tennis']})
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- scope `CreateFileMetadataByIdScope`
  - The scope of the metadata template. Example: "global"
- template_key `str`
  - The name of the metadata template. Example: "properties"
- request_body `Dict`
  - Request body of createFileMetadataById method
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataFull`.

Returns the instance of the template that was applied to the file,
including the data that was applied to the template.

## Update metadata instance on file

Updates a piece of metadata on a file.

The metadata instance can only be updated if the template has already been
applied to the file before. When editing metadata, only values that match
the metadata template schema will be accepted.

The update is applied atomically. If any errors occur during the
application of the operations, the metadata instance will not be changed.

This operation is performed by calling function `update_file_metadata_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-files-id-metadata-id-id/).

<!-- sample put_files_id_metadata_id_id -->

```python
client.file_metadata.update_file_metadata_by_id(file.id, UpdateFileMetadataByIdScope.ENTERPRISE, template_key, [UpdateFileMetadataByIdRequestBody(op=UpdateFileMetadataByIdRequestBodyOpField.REPLACE, path='/name', value='Jack'), UpdateFileMetadataByIdRequestBody(op=UpdateFileMetadataByIdRequestBodyOpField.REPLACE, path='/age', value=24), UpdateFileMetadataByIdRequestBody(op=UpdateFileMetadataByIdRequestBodyOpField.REPLACE, path='/birthDate', value='2000-01-03T02:20:50.520Z'), UpdateFileMetadataByIdRequestBody(op=UpdateFileMetadataByIdRequestBodyOpField.REPLACE, path='/countryCode', value='CA'), UpdateFileMetadataByIdRequestBody(op=UpdateFileMetadataByIdRequestBodyOpField.REPLACE, path='/sports', value=['football'])])
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- scope `UpdateFileMetadataByIdScope`
  - The scope of the metadata template. Example: "global"
- template_key `str`
  - The name of the metadata template. Example: "properties"
- request_body `List[UpdateFileMetadataByIdRequestBody]`
  - Request body of updateFileMetadataById method
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataFull`.

Returns the updated metadata template instance, with the
custom template data included.

## Remove metadata instance from file

Deletes a piece of file metadata.

This operation is performed by calling function `delete_file_metadata_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-files-id-metadata-id-id/).

<!-- sample delete_files_id_metadata_id_id -->

```python
client.file_metadata.delete_file_metadata_by_id(file.id, DeleteFileMetadataByIdScope.ENTERPRISE, template_key)
```

### Arguments

- file_id `str`
  - The unique identifier that represents a file. The ID for any file can be determined by visiting a file in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/files/123` the `file_id` is `123`. Example: "12345"
- scope `DeleteFileMetadataByIdScope`
  - The scope of the metadata template. Example: "global"
- template_key `str`
  - The name of the metadata template. Example: "properties"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the metadata is
successfully deleted.
