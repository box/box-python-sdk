# MetadataCascadePoliciesManager

- [List metadata cascade policies](#list-metadata-cascade-policies)
- [Create metadata cascade policy](#create-metadata-cascade-policy)
- [Get metadata cascade policy](#get-metadata-cascade-policy)
- [Remove metadata cascade policy](#remove-metadata-cascade-policy)
- [Force-apply metadata cascade policy to folder](#force-apply-metadata-cascade-policy-to-folder)

## List metadata cascade policies

Retrieves a list of all the metadata cascade policies
that are applied to a given folder. This can not be used on the root
folder with ID `0`.

This operation is performed by calling function `get_metadata_cascade_policies`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-metadata-cascade-policies/).

<!-- sample get_metadata_cascade_policies -->

```python
client.metadata_cascade_policies.get_metadata_cascade_policies(folder.id)
```

### Arguments

- folder_id `str`
  - Specifies which folder to return policies for. This can not be used on the root folder with ID `0`.
- owner_enterprise_id `Optional[str]`
  - The ID of the enterprise ID for which to find metadata cascade policies. If not specified, it defaults to the current enterprise.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- offset `Optional[int]`
  - The offset of the item at which to begin the response. Queries with offset parameter value exceeding 10000 will be rejected with a 400 response.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataCascadePolicies`.

Returns a list of metadata cascade policies.

## Create metadata cascade policy

Creates a new metadata cascade policy that applies a given
metadata template to a given folder and automatically
cascades it down to any files within that folder.

In order for the policy to be applied a metadata instance must first
be applied to the folder the policy is to be applied to.

This operation is performed by calling function `create_metadata_cascade_policy`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-metadata-cascade-policies/).

<!-- sample post_metadata_cascade_policies -->

```python
client.metadata_cascade_policies.create_metadata_cascade_policy(
    folder.id, CreateMetadataCascadePolicyScope.ENTERPRISE, template_key
)
```

### Arguments

- folder_id `str`
  - The ID of the folder to apply the policy to. This folder will need to already have an instance of the targeted metadata template applied to it.
- scope `CreateMetadataCascadePolicyScope`
  - The scope of the targeted metadata template. This template will need to already have an instance applied to the targeted folder.
- template_key `str`
  - The key of the targeted metadata template. This template will need to already have an instance applied to the targeted folder. In many cases the template key is automatically derived of its display name, for example `Contract Template` would become `contractTemplate`. In some cases the creator of the template will have provided its own template key. Please [list the templates for an enterprise][list], or get all instances on a [file][file] or [folder][folder] to inspect a template's key. [list]: https://developer.box.com/reference/get-metadata-templates-enterprise [file]: https://developer.box.com/reference/get-files-id-metadata [folder]: https://developer.box.com/reference/get-folders-id-metadata
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataCascadePolicy`.

Returns a new of metadata cascade policy.

## Get metadata cascade policy

Retrieve a specific metadata cascade policy assigned to a folder.

This operation is performed by calling function `get_metadata_cascade_policy_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-metadata-cascade-policies-id/).

<!-- sample get_metadata_cascade_policies_id -->

```python
client.metadata_cascade_policies.get_metadata_cascade_policy_by_id(cascade_policy_id)
```

### Arguments

- metadata_cascade_policy_id `str`
  - The ID of the metadata cascade policy. Example: "6fd4ff89-8fc1-42cf-8b29-1890dedd26d7"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataCascadePolicy`.

Returns a metadata cascade policy.

## Remove metadata cascade policy

Deletes a metadata cascade policy.

This operation is performed by calling function `delete_metadata_cascade_policy_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-metadata-cascade-policies-id/).

<!-- sample delete_metadata_cascade_policies_id -->

```python
client.metadata_cascade_policies.delete_metadata_cascade_policy_by_id(cascade_policy_id)
```

### Arguments

- metadata_cascade_policy_id `str`
  - The ID of the metadata cascade policy. Example: "6fd4ff89-8fc1-42cf-8b29-1890dedd26d7"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the policy
is successfully deleted.

## Force-apply metadata cascade policy to folder

Force the metadata on a folder with a metadata cascade policy to be applied to
all of its children. This can be used after creating a new cascade policy to
enforce the metadata to be cascaded down to all existing files within that
folder.

This operation is performed by calling function `apply_metadata_cascade_policy`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-metadata-cascade-policies-id-apply/).

<!-- sample post_metadata_cascade_policies_id_apply -->

```python
client.metadata_cascade_policies.apply_metadata_cascade_policy(
    cascade_policy_id, ApplyMetadataCascadePolicyConflictResolution.OVERWRITE
)
```

### Arguments

- metadata_cascade_policy_id `str`
  - The ID of the cascade policy to force-apply. Example: "6fd4ff89-8fc1-42cf-8b29-1890dedd26d7"
- conflict_resolution `ApplyMetadataCascadePolicyConflictResolution`
  - Describes the desired behavior when dealing with the conflict where a metadata template already has an instance applied to a child. _ `none` will preserve the existing value on the file _ `overwrite` will force-apply the templates values over any existing values.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the API call was successful. The metadata
cascade operation will be performed asynchronously.

The API call will return directly, before the cascade operation
is complete. There is currently no API to check for the status of this
operation.
