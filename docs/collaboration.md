Collaborations
==============

Collaborations are used to share folders between users or groups. They also
define what permissions a user has for a folder.


Add a Collaboration
-------------------

You can add a collaboration on a folder or a file by calling
[`item.collaborate(accessible_by, role, can_view_path=None, notify=None, fields=None)`][collaborate].  Pass the
[`User`][user_class] or [`Group`][group_class] to collaborate the item with as the `accessible_by` parameter.  The
`role` parameter determines what permissions the collaborator will have on the folder.  This method returns a
[`Collaboration`][collaboration_class] object representing the new collaboration on the item.

```python
from boxsdk.object.collaboration import CollaborationRole

user = client.user(user_id='11111')
collaboration = client.folder(folder_id='22222').collaborate(user, CollaborationRole.VIEWER)

collaborator = collaboration.accessible_by
item = collaboration.item
has_accepted = 'has' if collaboration.status == 'accepted' else 'has not'
print('{0} {1} accepted the collaboration to folder "{2}"'.format(collaborator.name, has_accepted, item.name))
```

Alternatively, you can also invite a user with their email address.

```python
from boxsdk.object.collaboration import CollaborationRole

email_of_invitee = 'testuser@example.com'
collaboration = client.folder(folder_id='22222').collaborate_with_login(email_of_invitee, CollaborationRole.VIEWER)
```

[collaborate]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.collaborate
[user_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.user.User
[group_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.group.Group
[collaboration_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collaboration.Collaboration

Edit a Collaboration
--------------------

A collaboration can be edited by calling [`collaboration.update_info(role, status=None)`][update_info].  This method
returns an updated [`Collaboration`][collaboration_class] object, leaving the original unmodified.

```python
from boxsdk.object.collaboration import CollaborationRole, CollaborationStatus

collaboration = client.collaboration(collab_id='12345')
updated_collaboration = collaboration.update_info(CollaborationRole.EDITOR)
```

[update_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collaboration.Collaboration.update_info

Remove a Collaboration
----------------------

A collaboration can be removed by calling [`collaboration.delete()`][delete].  This will generally cause the user or
group associated with the collaboration to lose access to the item.  This method returns `True` to indicate that removal
succeeded.

```python
collaboration_id = '1111'
client.collaboration(collaboration_id).delete()
```

[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.delete

Get a Collaboration's Information
---------------------------------

To get information about a specific collaboration, call [`collaboration.get()`][get].  This method returns a new
[`Collaboration`][collaboration_class] with fields populated by data from the API.

```python
collaboration = client.collaboration(collab_id='12345').get()
```

[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

List Collaborations on a Folder or File
----------------------------------------

To retrieve all collaborations on a specified [`Folder`][folder_class] or [`File`][file_class], call
[`item.get_collaborations(limit=None, marker=None, fields=None)`][get_collaborations].  This method returns a
[`BoxObjectCollection`][box_object_collection] that you can use to iterate over all
[`Collaboration`][collaboration_class] objects in the collection.

```python
collaborations = client.folder(folder_id='22222').get_collaborations()
for collab in collaborations:
    target = collab.accessible_by
    print('{0} {1} is collaborated on the folder'.format(target.type.capitalize(), target.name))
```

```python
collaborations = client.file(file_id='11111').get_collaborations()
for collab in collaborations
    target = collab.accessible_by
    print('{0} {1} is collaborated on the file'.format(target.type.capitalize(), target.name))
```

[folder_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder
[file_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File
[get_collaborations]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.get_collaborations
[box_object_collection]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.pagination.html#boxsdk.pagination.box_object_collection.BoxObjectCollection

List Pending Collaborations
---------------------------

To retrieve all pending collaborations for the current user, call
[`client.get_pending_collaborations(limit=None, offset=None, fields=None)`][get_pending_collaborations].  The user can
accept or reject these collaborations.  This method returns a [`BoxObjectCollection`][box_object_collection] that you
can use to iterate over all pending [`Collaboration`][collaboration_class] objects in the collection.

```python
pending_collaborations = client.get_pending_collaborations()
for pending_collaboration in pending_collaborations:
    print('Collaboration {0} is pending'.format(pending_collaboration.id))
```

[get_pending_collaborations]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.get_pending_collaborations

Accept or Reject a Pending Collaboration
-----------------------------------------

To accept or reject a pending collaboration, call [`collaboration.accept()`][accept] or
[`collaboration.reject()`][reject].  These methods both return the updated [`Collaboration`][collaboration_class]
object, leaving the original unmodified.

```python
accepted_collab = client.collaboration(collab_id='12345').accept()

rejected_collab = client.collaboration(collab_id='98765').reject()
```

[accept]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collaboration.Collaboration.accept
[reject]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.collaboration.Collaboration.reject
