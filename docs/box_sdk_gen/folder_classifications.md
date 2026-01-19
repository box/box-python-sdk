# FolderClassificationsManager

- [Get classification on folder](#get-classification-on-folder)
- [Add classification to folder](#add-classification-to-folder)
- [Update classification on folder](#update-classification-on-folder)
- [Remove classification from folder](#remove-classification-from-folder)

## Get classification on folder

Retrieves the classification metadata instance that
has been applied to a folder.

This API can also be called by including the enterprise ID in the
URL explicitly, for example
`/folders/:id/enterprise_12345/securityClassification-6VMVochwUWo`.

This operation is performed by calling function `get_classification_on_folder`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-folders-id-metadata-enterprise-securityClassification-6VMVochwUWo/).

<!-- sample get_folders_id_metadata_enterprise_securityClassification-6VMVochwUWo -->

```python
client.folder_classifications.get_classification_on_folder(folder.id)
```

### Arguments

- folder_id `str`
  - The unique identifier that represent a folder. The ID for any folder can be determined by visiting this folder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/folder/123` the `folder_id` is `123`. The root folder of a Box account is always represented by the ID `0`. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Classification`.

Returns an instance of the `securityClassification` metadata
template, which contains a `Box__Security__Classification__Key`
field that lists all the classifications available to this
enterprise.

## Add classification to folder

Adds a classification to a folder by specifying the label of the
classification to add.

This API can also be called by including the enterprise ID in the
URL explicitly, for example
`/folders/:id/enterprise_12345/securityClassification-6VMVochwUWo`.

This operation is performed by calling function `add_classification_to_folder`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-folders-id-metadata-enterprise-securityClassification-6VMVochwUWo/).

<!-- sample post_folders_id_metadata_enterprise_securityClassification-6VMVochwUWo -->

```python
client.folder_classifications.add_classification_to_folder(folder.id, box_security_classification_key=classification.key)
```

### Arguments

- folder_id `str`
  - The unique identifier that represent a folder. The ID for any folder can be determined by visiting this folder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/folder/123` the `folder_id` is `123`. The root folder of a Box account is always represented by the ID `0`. Example: "12345"
- box_security_classification_key `Optional[str]`
  - The name of the classification to apply to this folder. To list the available classifications in an enterprise, use the classification API to retrieve the [classification template](https://developer.box.com/reference/get-metadata-templates-enterprise-securityClassification-6VMVochwUWo-schema) which lists all available classification keys.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Classification`.

Returns the classification template instance
that was applied to the folder.

## Update classification on folder

Updates a classification on a folder.

The classification can only be updated if a classification has already been
applied to the folder before. When editing classifications, only values are
defined for the enterprise will be accepted.

This operation is performed by calling function `update_classification_on_folder`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-folders-id-metadata-enterprise-securityClassification-6VMVochwUWo/).

<!-- sample put_folders_id_metadata_enterprise_securityClassification-6VMVochwUWo -->

```python
client.folder_classifications.update_classification_on_folder(folder.id, [UpdateClassificationOnFolderRequestBody(value=second_classification.key)])
```

### Arguments

- folder_id `str`
  - The unique identifier that represent a folder. The ID for any folder can be determined by visiting this folder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/folder/123` the `folder_id` is `123`. The root folder of a Box account is always represented by the ID `0`. Example: "12345"
- request_body `List[UpdateClassificationOnFolderRequestBody]`
  - Request body of updateClassificationOnFolder method
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `Classification`.

Returns the updated classification metadata template instance.

## Remove classification from folder

Removes any classifications from a folder.

This API can also be called by including the enterprise ID in the
URL explicitly, for example
`/folders/:id/enterprise_12345/securityClassification-6VMVochwUWo`.

This operation is performed by calling function `delete_classification_from_folder`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-folders-id-metadata-enterprise-securityClassification-6VMVochwUWo/).

<!-- sample delete_folders_id_metadata_enterprise_securityClassification-6VMVochwUWo -->

```python
client.folder_classifications.delete_classification_from_folder(folder.id)
```

### Arguments

- folder_id `str`
  - The unique identifier that represent a folder. The ID for any folder can be determined by visiting this folder in the web application and copying the ID from the URL. For example, for the URL `https://*.app.box.com/folder/123` the `folder_id` is `123`. The root folder of a Box account is always represented by the ID `0`. Example: "12345"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the classification is
successfully deleted.
