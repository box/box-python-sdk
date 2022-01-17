Metadata
========

Metadata allows users and applications to define and store custom data associated
with their files/folders. Metadata consists of key:value pairs that belong to
files/folders. For example, an important contract may have key:value pairs of
`"clientNumber":"820183"` and `"clientName":"bioMedicalCorp"`.

Metadata that belongs to a file/folder is grouped by templates. Templates allow
the metadata service to provide a multitude of services, such as pre-defining sets
of key:value pairs or schema enforcement on specific fields.

Each file/folder can have multiple distinct template instances associated with it,
and templates are also grouped by scopes. Currently, the only scopes support are
`enterprise` and `global`. Enterprise scopes are defined on a per enterprises basis,
whereas global scopes are Box application-wide.

In addition to `enterprise` scoped templates, every file on Box has access to the
`global` `properties` template. The Properties template is a bucket of free form
key:value string pairs, with no additional schema associated with it. Properties
are ideal for scenarios where applications want to write metadata to file objects
in a flexible way, without pre-defined template structure.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Create Metadata Template](#create-metadata-template)
- [Get Metadata Template](#get-metadata-template)
  - [Get by scope and template key](#get-by-scope-and-template-key)
  - [Get by template ID](#get-by-template-id)
- [Update Metadata Template](#update-metadata-template)
- [Get Enterprise Metadata Templates](#get-enterprise-metadata-templates)
- [Delete Metadata Template](#delete-metadata-template)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Create Metadata Template
------------------------

To create a new metadata template, call
[`client.create_metadata_template(display_name, fields, template_key=None, hidden=False, scope='enterprise', copy_instance_on_item_copy=False)`][create_template]
with the human-readable name of the template and the [`MetadataField`s][metadata_field_class] the template should have.
You can optionally specify a key for the template, otherwise one will be derived from the display name.  At the current
time, only `enterprise` scope templates are supported.  This method returns a
[`MetadataTemplate`][metadata_template_class] object representing the created template.

<!-- sample post_metadata_templates_schema -->
```python
from boxsdk.object.metadata_template import MetadataField, MetadataFieldType

fields = [
    MetadataField(MetadataFieldType.STRING, 'Name')
    MetadataField(MetadataFieldType.DATE, 'Birthday', 'bday')
    MetadataField(MetadataFieldType.ENUM, 'State', options=['CA', 'TX', 'NY'])
]
template = client.create_metadata_template('Employee Record', fields, hidden=True)
print(f'Metadata template ID {template.scope}/{template.templateKey} created!')
```

[create_template]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.create_metadata_template
[metadata_field_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata_template.MetadataField
[metadata_template_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata_template.MetadataTemplate

Get Metadata Template
---------------------

### Get by scope and template key

To retrieve a specific template by scope and template key, first use
[`client.metadata_template(scope, template_key)`][metadata_template] to construct the appropriate
[`MetadataTemplate`][metadata_template_class] object, and then call [`template.get()`][get] to retrieve data about
the template.  This method returns a new [`MetadataTemplate`][metadata_template_class] object with fields populated by
data from the API, leaving the original object unmodified.

<!-- sample get_metadata_templates_id_id_schema -->
```python
template = client.metadata_template('enterprise', 'employeeRecord').get()
print(f'The {template.displayName} template has {len(template.fields)} fields')
```

[metadata_template]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.metadata_template
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

### Get by template ID

To retrieve a template by ID, call [`client.get_metadata_template_by_id(template_id)`][get_by_id] with the ID of the
metadata template.  This method returns a [`MetadataTemplate`][metadata_template_class] object with fields populated by
data from the API.

<!-- sample get_metadata_templates_id -->
```python
template = client.metadata_template_by_id(template_id='abcdef-fba434-ace44').get()
print(f'The {template.displayName} template has {len(template.fields)} fields')
```

[get_by_id]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.get_metadata_template_by_id

Update Metadata Template
------------------------

To make changes to a metadata template, first call [`template.start_update()`][start_update] to create a
[`MetadataTemplateUpdate`][template_update_class] to track updates.  Call the methods on this object to add the
necessary update operations, and then call [`template.update_info(*, updates, **kwargs)`][update_info] with the updates
object to apply the changes to the metadata template.  This method returns an updated
[`MetadataTemplate`][metadata_template_class] object with the changes applied, leaving the original object unmodified.

<!-- sample put_metadata_templates_id_id_schema -->
```python
template = client.metadata_template('enterprise', 'employeeRecord')
updates = template.start_update()
updates.add_enum_option('state', 'WI')
updates.edit_template({'hidden': False})
updates.edit_template({'copyInstanceOnItemCopy': False})
updated_template = template.update_info(updates=updates)
```

[start_update]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata_template.MetadataTemplate.start_update
[template_update_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata_template.MetadataTemplateUpdate
[update_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata_template.MetadataTemplate.update_info

Get Enterprise Metadata Templates
---------------------------------

Get all metadata templates for the current enterprise by calling
[`client.get_metadata_templates(scope='enterprise', limit=None, marker=None, fields=None)`][get_metadata_templates].
By default, this retrieves all templates scoped to the current enterprise, but you can pass the `scope` parameter to
retrieve templates for a different scope.  This method returns a [`BoxObjectCollection`][box_object_collection] that
allows you to iterate over all the [`MetadataTemplate`][metadata_template_class] objects in the collection.

<!-- sample get_metadata_templates_enterprise -->
```python
templates = client.get_metadata_templates()
for template in templates:
    print(f'Metadata template {template.templateKey} is in enterprise scope')
```

To return the metadata templates available to all enterprises pass in the
`global` scope.

<!-- sample get_metadata_templates_global -->
```python
templates = client.get_metadata_templates(scope='global)
for template in templates:
    print(f'Metadata template {template.templateKey} is in global scope')
```

[get_metadata_templates]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.get_metadata_templates
[box_object_collection]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.pagination.html#boxsdk.pagination.box_object_collection.BoxObjectCollection

Delete Metadata Template
------------------------

To delete a metadata template, call [`template.delete()`][delete].  This method returns `True` to indicate the deletion
was successful.

<!-- sample delete_metadata_templates_id_id_schema -->
```python
client.metadata_template('enterprise', 'employeeRecord').delete()
```

[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.delete
