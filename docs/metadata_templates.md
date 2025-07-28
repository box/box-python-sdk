# MetadataTemplatesManager

- [Find metadata template by instance ID](#find-metadata-template-by-instance-id)
- [Get metadata template by name](#get-metadata-template-by-name)
- [Update metadata template](#update-metadata-template)
- [Remove metadata template](#remove-metadata-template)
- [Get metadata template by ID](#get-metadata-template-by-id)
- [List all global metadata templates](#list-all-global-metadata-templates)
- [List all metadata templates for enterprise](#list-all-metadata-templates-for-enterprise)
- [Create metadata template](#create-metadata-template)

## Find metadata template by instance ID

Finds a metadata template by searching for the ID of an instance of the
template.

This operation is performed by calling function `get_metadata_templates_by_instance_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-metadata-templates/).

<!-- sample get_metadata_templates -->

```python
client.metadata_templates.get_metadata_templates_by_instance_id(
    created_metadata_instance.id
)
```

### Arguments

- metadata_instance_id `str`
  - The ID of an instance of the metadata template to find.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTemplates`.

Returns a list containing the 1 metadata template that matches the
instance ID.

## Get metadata template by name

Retrieves a metadata template by its `scope` and `templateKey` values.

To find the `scope` and `templateKey` for a template, list all templates for
an enterprise or globally, or list all templates applied to a file or folder.

This operation is performed by calling function `get_metadata_template`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-metadata-templates-id-id-schema/).

<!-- sample get_metadata_templates_id_id_schema -->

```python
client.metadata_templates.get_metadata_template(
    GetMetadataTemplateScope.ENTERPRISE, template.template_key
)
```

### Arguments

- scope `GetMetadataTemplateScope`
  - The scope of the metadata template. Example: "global"
- template_key `str`
  - The name of the metadata template. Example: "properties"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTemplate`.

Returns the metadata template matching the `scope`
and `template` name.

## Update metadata template

Updates a metadata template.

The metadata template can only be updated if the template
already exists.

The update is applied atomically. If any errors occur during the
application of the operations, the metadata template will not be changed.

This operation is performed by calling function `update_metadata_template`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-metadata-templates-id-id-schema/).

<!-- sample put_metadata_templates_id_id_schema -->

```python
client.metadata_templates.update_metadata_template(
    UpdateMetadataTemplateScope.ENTERPRISE,
    template_key,
    [
        UpdateMetadataTemplateRequestBody(
            op=UpdateMetadataTemplateRequestBodyOpField.ADDFIELD,
            field_key="newfieldname",
            data={"type": "string", "displayName": "newFieldName"},
        )
    ],
)
```

### Arguments

- scope `UpdateMetadataTemplateScope`
  - The scope of the metadata template. Example: "global"
- template_key `str`
  - The name of the metadata template. Example: "properties"
- request_body `List[UpdateMetadataTemplateRequestBody]`
  - Request body of updateMetadataTemplate method
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTemplate`.

Returns the updated metadata template, with the
custom template data included.

## Remove metadata template

Delete a metadata template and its instances.
This deletion is permanent and can not be reversed.

This operation is performed by calling function `delete_metadata_template`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-metadata-templates-id-id-schema/).

<!-- sample delete_metadata_templates_id_id_schema -->

```python
client.metadata_templates.delete_metadata_template(
    DeleteMetadataTemplateScope.ENTERPRISE, template.template_key
)
```

### Arguments

- scope `DeleteMetadataTemplateScope`
  - The scope of the metadata template. Example: "global"
- template_key `str`
  - The name of the metadata template. Example: "properties"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `None`.

Returns an empty response when the metadata
template is successfully deleted.

## Get metadata template by ID

Retrieves a metadata template by its ID.

This operation is performed by calling function `get_metadata_template_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-metadata-templates-id/).

<!-- sample get_metadata_templates_id -->

```python
client.metadata_templates.get_metadata_template_by_id(template.id)
```

### Arguments

- template_id `str`
  - The ID of the template. Example: "f7a9891f"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTemplate`.

Returns the metadata template that matches the ID.

## List all global metadata templates

Used to retrieve all generic, global metadata templates available to all
enterprises using Box.

This operation is performed by calling function `get_global_metadata_templates`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-metadata-templates-global/).

<!-- sample get_metadata_templates_global -->

```python
client.metadata_templates.get_global_metadata_templates()
```

### Arguments

- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTemplates`.

Returns all of the metadata templates available to all enterprises
and their corresponding schema.

## List all metadata templates for enterprise

Used to retrieve all metadata templates created to be used specifically within
the user's enterprise.

This operation is performed by calling function `get_enterprise_metadata_templates`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-metadata-templates-enterprise/).

<!-- sample get_metadata_templates_enterprise -->

```python
client.metadata_templates.get_enterprise_metadata_templates()
```

### Arguments

- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination. This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTemplates`.

Returns all of the metadata templates within an enterprise
and their corresponding schema.

## Create metadata template

Creates a new metadata template that can be applied to
files and folders.

This operation is performed by calling function `create_metadata_template`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-metadata-templates-schema/).

<!-- sample post_metadata_templates_schema -->

```python
client.metadata_templates.create_metadata_template(
    "enterprise",
    template_key,
    template_key=template_key,
    fields=[
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.STRING,
            key="testName",
            display_name="testName",
        ),
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.FLOAT,
            key="age",
            display_name="age",
        ),
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.DATE,
            key="birthDate",
            display_name="birthDate",
        ),
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.ENUM,
            key="countryCode",
            display_name="countryCode",
            options=[
                CreateMetadataTemplateFieldsOptionsField(key="US"),
                CreateMetadataTemplateFieldsOptionsField(key="CA"),
            ],
        ),
        CreateMetadataTemplateFields(
            type=CreateMetadataTemplateFieldsTypeField.MULTISELECT,
            key="sports",
            display_name="sports",
            options=[
                CreateMetadataTemplateFieldsOptionsField(key="basketball"),
                CreateMetadataTemplateFieldsOptionsField(key="football"),
                CreateMetadataTemplateFieldsOptionsField(key="tennis"),
            ],
        ),
    ],
)
```

### Arguments

- scope `str`
  - The scope of the metadata template to create. Applications can only create templates for use within the authenticated user's enterprise. This value needs to be set to `enterprise`, as `global` scopes can not be created by applications.
- template_key `Optional[str]`
  - A unique identifier for the template. This identifier needs to be unique across the enterprise for which the metadata template is being created. When not provided, the API will create a unique `templateKey` based on the value of the `displayName`.
- display_name `str`
  - The display name of the template.
- hidden `Optional[bool]`
  - Defines if this template is visible in the Box web app UI, or if it is purely intended for usage through the API.
- fields `Optional[List[CreateMetadataTemplateFields]]`
  - An ordered list of template fields which are part of the template. Each field can be a regular text field, date field, number field, as well as a single or multi-select list.
- copy_instance_on_item_copy `Optional[bool]`
  - Whether or not to copy any metadata attached to a file or folder when it is copied. By default, metadata is not copied along with a file or folder when it is copied.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `MetadataTemplate`.

The schema representing the metadata template created.
