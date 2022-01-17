Metadata Cascade Policies
=========================

Metadata Cascade Policies allow the metadata values on a folder to be applied to the files within that folder.  A
cascade policy associates the folder with a specific metadata template whose instance values on the folder should be
cascaded to files within the folder.

> __Note:__ The Metadata Cascade Policy endpoints are currently in beta. Please email
> [betas+metadata@box.com](mailto:betas+metadata@box.com) if you would like to enable this beta feature for your
> enterprise.  If you do not have this enabled for your enterprise, you will get a 403 error.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Create a Metadata Cascade Policy](#create-a-metadata-cascade-policy)
- [Get Information About a Metadata Cascade Policy](#get-information-about-a-metadata-cascade-policy)
- [Get Cascade Policies on a Folder](#get-cascade-policies-on-a-folder)
- [Force Apply Cascade Policy](#force-apply-cascade-policy)
- [Remove Cascade Policy](#remove-cascade-policy)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Create a Metadata Cascade Policy
--------------------------------

To create a metadata cascade policy on a folder, call [`folder.cascade_metadata(metadata_template)`][cascade_metadata]
with the [`MetadataTemplate`][metadata_template_class] whose values should be cascaded within the folder.  This
method returns a [`MetadataCascadePolicy`][cascade_policy_class] object representing the newly-created policy.

<!-- sample post_metadata_cascade_policies -->
```python
folder = client.folder(folder_id='22222')
metadata_template = client.metadata_template('enterprise', 'securityClassiciation')

cascade_policy = folder.cascade_metadata(metadata_template)
print(f'Folder {cascade_policy.parent.id} has a metadata cascade policy for {cascade_policy.scope} template "{cascade_policy.templateKey}"')
```

[cascade_metadata]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder.cascade_metadata
[metadata_template_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata_template.MetadataTemplate
[cascade_policy_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata_cascade_policy.MetadataCascadePolicy

Get Information About a Metadata Cascade Policy
-----------------------------------------------

To retrieve information about a metadata cascade policy, first call
[`client.metadata_cascade_policy(policy_id)`][initializer] with the ID of the cascade policy to initialize the
[`MetadataCascadePolicy`][cascade_policy_class] object, then call [`cascade_policy.get()`][get] to retrieve data about
the policy.  This method returns a new [`MetadataCascadePolicy`][cascade_policy_class] object with fields populated by
data from the API, leaving the original object unmodified.

<!-- sample get_metadata_cascade_policies_id -->
```python
cascade_policy = client.metadata_cascade_policy('84113349-794d-445c-b93c-d8481b223434').get()
print(f'Cascade policy applies to a template owned by enterprise {cascade_policy.owner_enterprise.id}')
```

[initializer]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.metadata_cascade_policy
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

Get Cascade Policies on a Folder
--------------------------------

To get a list of the cascade policies applied to a folder, call
[`folder.get_metadata_cascade_policies(owner_enterprise=None, limit=None, marker=None, fields=None)`][get_metadata_cascade_policies].
You can optionally pass an [`Enterprise`][enterprise_class] object via the `owner_enterprise` parameter to retrieve
cascade policies related to templates for a specific enterprise; if not specified, this defaults to the current
enterprise.  This method returns a [`BoxObjectCollection`][box_object_collection] that allows you to iterate over the
[`MetadataCascadePolicy`][cascade_policy_class] objects in the collection.

<!-- sample get_metadata_cascade_policies -->
```python
cascade_policies = client.folder(folder_id='22222').get_metadata_cascade_policies()
for policy in cascade_policies:
    print(f'Metadata template {policy.templateKey} is cascaded')
```

[get_metadata_cascade_policies]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder.get_metadata_cascade_policies
[enterprise_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.enterprise.Enterprise
[box_object_collection]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.pagination.html#boxsdk.pagination.box_object_collection.BoxObjectCollection

Force Apply Cascade Policy
--------------------------

A Cascade Policy can be forced to re-apply to all files in the associated folder by calling
[`cascade_policy.force_apply(conflict_resolution)`][force_apply] with the conflict resolution strategy to use.  If
files in the folder already have metadata values that conflict with the ones being force applied from the folder, you
can choose to either preserve the existing values or overwrite them with the folder's values.  This method returns
`True` to indicate that the force application was successful.

<!-- sample post_metadata_cascade_policies_id_apply -->
```python
from boxsdk.object.metadata_cascade_policy import CascadePolicyConflictResolution

cascade_policy = client.metadata_cascade_policy(policy_id='84113349-794d-445c-b93c-d8481b223434')
cascade_policy.force_apply(CascadePolicyConflictResolution.PRESERVE_EXISTING)
print('Cascade policy was force applied!')
```

[force_apply]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata_cascade_policy.MetadataCascadePolicy.force_apply

Remove Cascade Policy
---------------------

A metadata cascade policy can be removed from a folder by calling [`cascade_policy.delete()`][delete].  This method
returns `True` to indicate that the deletion was successful.

<!-- sample delete_metadata_cascade_policies_id -->
```python
client.metadata_cascade_policy(policy_id='84113349-794d-445c-b93c-d8481b223434').delete()
print('Cascade policy successfully removed')
```

[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.delete
