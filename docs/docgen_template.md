# DocgenTemplateManager

- [Create Box Doc Gen template](#create-box-doc-gen-template)
- [List Box Doc Gen templates](#list-box-doc-gen-templates)
- [Delete Box Doc Gen template](#delete-box-doc-gen-template)
- [Get Box Doc Gen template by ID](#get-box-doc-gen-template-by-id)
- [List all Box Doc Gen template tags in template](#list-all-box-doc-gen-template-tags-in-template)
- [Get list of all Box Doc Gen jobs for template](#get-list-of-all-box-doc-gen-jobs-for-template)

## Create Box Doc Gen template

Marks a file as a Box Doc Gen template.

This operation is performed by calling function `create_docgen_template_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/post-docgen-templates/).

<!-- sample post_docgen_templates_v2025.0 -->

```python
client.docgen_template.create_docgen_template_v2025_r0(FileReferenceV2025R0(id=file.id))
```

### Arguments

- file `FileReferenceV2025R0`
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `DocGenTemplateBaseV2025R0`.

The file which has now been marked as a Box Doc Gen template.

## List Box Doc Gen templates

Lists Box Doc Gen templates on which the user is a collaborator.

This operation is performed by calling function `get_docgen_templates_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/get-docgen-templates/).

<!-- sample get_docgen_templates_v2025.0 -->

```python
client.docgen_template.get_docgen_templates_v2025_r0()
```

### Arguments

- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `DocGenTemplatesV2025R0`.

Returns a collection of templates.

## Delete Box Doc Gen template

Unmarks file as Box Doc Gen template.

This operation is performed by calling function `delete_docgen_template_by_id_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/delete-docgen-templates-id/).

<!-- sample delete_docgen_templates_id_v2025.0 -->

```python
client.docgen_template.delete_docgen_template_by_id_v2025_r0(
    created_docgen_template.file.id
)
```

### Arguments

- template_id `str`
  - ID of the file which will no longer be marked as a Box Doc Gen template. Example: "123"
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when a file is no longer marked as a Box Doc Gen template.

## Get Box Doc Gen template by ID

Lists details of a specific Box Doc Gen template.

This operation is performed by calling function `get_docgen_template_by_id_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/get-docgen-templates-id/).

<!-- sample get_docgen_templates_id_v2025.0 -->

```python
client.docgen_template.get_docgen_template_by_id_v2025_r0(
    created_docgen_template.file.id
)
```

### Arguments

- template_id `str`
  - The ID of a Box Doc Gen template. Example: 123
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `DocGenTemplateV2025R0`.

Returns a template.

## List all Box Doc Gen template tags in template

Lists all tags in a Box Doc Gen template.

This operation is performed by calling function `get_docgen_template_tags_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/get-docgen-templates-id-tags/).

<!-- sample get_docgen_templates_id_tags_v2025.0 -->

```python
client.docgen_template.get_docgen_template_tags_v2025_r0(
    fetched_docgen_template.file.id
)
```

### Arguments

- template_id `str`
  - ID of template. Example: 123
- template_version_id `Optional[str]`
  - Id of template version.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `DocGenTagsV2025R0`.

A list of document generation template tags.Processing tags for the file.

## Get list of all Box Doc Gen jobs for template

Lists the users jobs which use this template.

This operation is performed by calling function `get_docgen_template_job_by_id_v2025_r0`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/v2025.0/get-docgen-template-jobs-id/).

<!-- sample get_docgen_template_jobs_id_v2025.0 -->

```python
client.docgen_template.get_docgen_template_job_by_id_v2025_r0(
    fetched_docgen_template.file.id
)
```

### Arguments

- template_id `str`
  - Id of template to fetch jobs for. Example: 123
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- box_version `BoxVersionHeaderV2025R0`
  - Version header.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `DocGenJobsV2025R0`.

A single Box Doc Gen template.
