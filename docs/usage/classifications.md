Classifications
===============

Classifications are a type of metadata that allows users and applications 
to define and assign a content classification to files and folders.

Classifications use the metadata APIs to add and remove classifications, and
assign them to files. For more details on metadata templates please see the
[metadata documentation](./metadata.md).

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Add initial classifications](#add-initial-classifications)
- [List all classifications](#list-all-classifications)
- [Add another classification](#add-another-classification)
- [Update a classification](#update-a-classification)
- [Delete a classification](#delete-a-classification)
- [Delete all classifications](#delete-all-classifications)
- [Add classification to file](#add-classification-to-file)
- [Update classification on file](#update-classification-on-file)
- [Get classification on file](#get-classification-on-file)
- [Remove classification from file](#remove-classification-from-file)
- [Add classification to folder](#add-classification-to-folder)
- [Update classification on folder](#update-classification-on-folder)
- [Get classification on folder](#get-classification-on-folder)
- [Remove classification from folder](#remove-classification-from-folder)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Add initial classifications
---------------------------

If an enterprise does not already have a classification defined, the first classification(s)
can be added with the
`client.create_metadata_template(display_name, fields, template_key=None, hidden=False, scope='enterprise')`](https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.create_metadata_template)
method.

<!-- sample post_metadata_templates_schema classifications -->
```python 
from boxsdk.object.metadata_template import MetadataField, MetadataFieldType

fields = [
    MetadataField(MetadataFieldType.ENUM, 'Classification', key='Box__Security__Classification__Key', options=['Top Secret'])
]

template = client.create_metadata_template('Classification', fields, template_key='securityClassification-6VMVochwUWo')
```

List all classifications
------------------------

To retrieve a list of all the classifications in an enterprise call the
[`client.metadata_template(scope, template_key)`](https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.metadata_template)
method to get the classifications template, which will contain a list of all the 
classifications.

<!-- sample get_metadata_templates_enterprise_securityClassification-6VMVochwUWo_schema -->
```python
template = client.metadata_template('enterprise', 'securityClassification-6VMVochwUWo').get()
```

Add another classification
--------------------------

To add another classification, call the
[`template.start_update()`][start_update] API to start making changes to the 
template, and then call the [`template.update_info(updates=new_updates)`][update_info]
with the changes to apply to the template.

<!-- sample put_metadata_templates_enterprise_securityClassification-6VMVochwUWo_schema add -->
```python
template = client.metadata_template('enterprise', 'securityClassification-6VMVochwUWo')
new_updates = template.start_update()
new_updates.add_enum_option('Box__Security__Classification__Key', 'Sensitive')
updated_template = template.update_info(updates=new_updates)
```

[start_update]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata_template.MetadataTemplate.start_update
[update_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata_template.MetadataTemplate.update_info

Update a classification
-----------------------

To update a classification, call the
[`template.start_update()`][start_update] API to start making changes to the 
template, and then call the [`template.update_info(updates=new_updates)`][update_info]
with the classification to change on the template.

<!-- sample put_metadata_templates_enterprise_securityClassification-6VMVochwUWo_schema update -->
```python
template = client.metadata_template('enterprise', 'securityClassification-6VMVochwUWo')
new_updates = template.start_update()
new_updates.edit_enum_option('Box__Security__Classification__Key', 'Sensitive', 'Very Sensitive')
updated_template = template.update_info(updates=new_updates)
```

Delete a classification
-----------------------

To delete a classification, call the
[`template.start_update()`][start_update] API to start making changes to the 
template, and then call the [`template.update_info(updates=new_updates)`][update_info]
with the classification to remove from the template.

<!-- sample put_metadata_templates_enterprise_securityClassification-6VMVochwUWo_schema delete -->
```python
template = client.metadata_template('enterprise', 'securityClassification-6VMVochwUWo')
new_updates = template.start_update()
new_updates.remove_enum_option('Box__Security__Classification__Key', 'Sensitive')
updated_template = template.update_info(updates=new_updates)
```

Delete all classifications
--------------------------

To remove all classifications in an enterprise, call the
[`template.delete()`](https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.delete)
method with the name of the classification metadata template. 

<!-- sample delete_metadata_templates_enterprise_securityClassification-6VMVochwUWo_schema -->
```python
client.metadata_template('enterprise', 'securityClassification-6VMVochwUWo').delete()
```

Add classification to file
--------------------------

To add a classification to a file, call 
[`file.metadata(scope='global', template='properties')`][set-metadata]
with the name of the classification template, as well as the details of the classification
to add to the file.

<!-- sample post_files_id_metadata_enterprise_securityClassification-6VMVochwUWo -->
```python
classification = {
    'Box__Security__Classification__Key': 'Sensitive',
}
applied_metadata = client.file(file_id='11111').metadata(scope='enterprise', template='securityClassification-6VMVochwUWo').set(classification)
```

[set-metadata]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.metadata

Update classification on file
-----------------------------

To update a classification on a file, call 
[`file.metadata(scope='global', template='properties')`][update-metadata]
with the name of the classification template, as well as the details of the classification
to add to the file.

<!-- sample put_files_id_metadata_enterprise_securityClassification-6VMVochwUWo -->
```python
classification = {
    'Box__Security__Classification__Key': 'Sensitive',
}
applied_metadata = client.file(file_id='11111').metadata(scope='enterprise', template='securityClassification-6VMVochwUWo').set(classification)
```

[update-metadata]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.metadata

Get classification on file
--------------------------

Retrieve the classification on a file by calling
[`file.metadata(scope='global', template='properties').get()`](https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata.Metadata.get)
on a file.

<!-- sample get_files_id_metadata_enterprise_securityClassification-6VMVochwUWo -->
```python
metadata = client.file(file_id='11111').metadata(scope='enterprise', template='securityClassification-6VMVochwUWo').get()
```

Remove classification from file
-------------------------------

A classification can be removed from a file by calling
[`file.metadata(scope='global', template='properties').delete()`](https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata.Metadata.delete).

<!-- sample delete_files_id_metadata_enterprise_securityClassification-6VMVochwUWo -->
```python
client.file(file_id='11111').metadata(scope='securityClassification-6VMVochwUWo', template='myMetadata').delete()
```



Add classification to folder
--------------------------

To add a classification to a folder, call 
[`folder.metadata(scope='global', template='properties')`][set-metadata]
with the name of the classification template, as well as the details of the classification
to add to the folder.

<!-- sample post_folders_id_metadata_enterprise_securityClassification-6VMVochwUWo -->
```python
classification = {
    'Box__Security__Classification__Key': 'Sensitive',
}
applied_metadata = client.folder(folder_id='11111').metadata(scope='enterprise', template='securityClassification-6VMVochwUWo').set(classification)
```

[set-metadata]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.metadata

Update classification on folder
-----------------------------

To update a classification on a folder, call 
[`folder.metadata(scope='global', template='properties')`][update-metadata]
with the name of the classification template, as well as the details of the classification
to add to the folder.

<!-- sample put_folders_id_metadata_enterprise_securityClassification-6VMVochwUWo -->
```python
classification = {
    'Box__Security__Classification__Key': 'Sensitive',
}
applied_metadata = client.folder(folder_id='11111').metadata(scope='enterprise', template='securityClassification-6VMVochwUWo').set(classification)
```

[update-metadata]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.metadata

Get classification on folder
--------------------------

Retrieve the classification on a folder by calling
[`folder.metadata(scope='global', template='properties').get()`](https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata.Metadata.get)
on a folder.

<!-- sample get_folders_id_metadata_enterprise_securityClassification-6VMVochwUWo -->
```python
metadata = client.folder(folder_id='11111').metadata(scope='enterprise', template='securityClassification-6VMVochwUWo').get()
```

Remove classification from folder
-------------------------------

A classification can be removed from a folder by calling
[`folder.metadata(scope='global', template='properties').delete()`](https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata.Metadata.delete).

<!-- sample delete_folders_id_metadata_enterprise_securityClassification-6VMVochwUWo -->
```python
client.folder(folder_id='11111').metadata(scope='securityClassification-6VMVochwUWo', template='myMetadata').delete()
```
