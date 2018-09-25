Collaborations
==============

Collaborations are used to share folders between users or groups. They also
define what permissions a user has for a folder.


Add a Collaboration
-------------------

You can add a collaboration on a folder or a file by calling `item.collaborate(accessible_by, role, can_view_path=None, notify=None, fields=None)`. The
`role` parameter determines what permissions the collaborator will have on the folder.

```python
from boxsdk.object.collaboration import CollaborationRole
folder_id = '1234'
user_id = '1111'
collaborator = client.user(user_id)
collaboration = client.folder(folder_id).collaborate(collaborator, CollaborationRole.VIEWER)
```

Alternatively you can also invite a user with their email address.

```python
from boxsdk.object.collaboration import CollaborationRole
folder_id = '1234'
email_of_invitee = 'testuser@example.com'
collaboration = client.folder(folder_id).collaborate_with_login(email_of_invitee, CollaborationRole.VIEWER)
```

Edit a Collaboration
--------------------

A collaboration can be edited by using `collaboration.update_info()`.

```python
from boxsdk.object.collaboration import CollaborationRole, CollaborationStatus
updated_collaboration = client.collaboration('1111').update_info(CollaborationRole.EDITOR, CollaborationStatus.ACCEPTED)
```

Remove a Collaboration
----------------------

A collaboration can be removed by calling `collaboration.delete()`.

```python
collaboration_id = '1111'
collaboration = client.collaboration(collaboration_id).delete()
```

Get a Collaboration's Information
---------------------------------

To get information about a specific collaboration use `collaboration.get()`.

```python
collaboration_id = '1111'
collaboration_info = client.collaboration(collaboration_id).get()
```

List Collaborations on a Folder or File
----------------------------------------

To retrieve all collaborations on a specified folder you can use `folder.get_collaborations(limit=None, marker=None, fields=None)`. Or to retrieve an iterable of collaborations on a specified file you can use `file.get_collaborations(limit=None, marker=None, fields=None)`.

```python
folder_id = '1234'
collaborations = client.folder(folder_id).get_collaborations()
for collaboration in collaborations:
    # Do something
```

```python
file_id = '2222'
collaborations = client.file(file_id).get_collaborations()
for collaboration in collaborations
    # Do something
```

List Pending Collaborations
---------------------------

To retrieve all pending collaborations for the user, use `client.get_pending_collaborations(limit=None, offset=None, fields=None)`.

```python
pending_collaborations = client.get_pending_collaborations()
for pending_collaboration in pending_collaborations:
    # Do something
```

Accept or Reject a Pending Collaboration
-----------------------------------------

To `accept` or `reject` a pending collaboration use `collaboration.accept()` or `collaboration.reject()`.

```python
collaboration_id = '3333'
updated_collaboration = client.collaboration(collaboration_id).accept()
```

You can reject a pending collaboration with

```python
collaboration_id = '3333'
updated_collaboration = client.collaboration(collaboration_id).reject()
```
