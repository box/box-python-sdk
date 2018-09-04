Collaborations
==============

Collaborations are used to share folders between users or groups. They also
define what permissions a user has for a folder.

- [Add a Collaboration](#add-a-collaboration)
- [Edit a Collaboration](#edit-a-collaboration)
- [Remove a Collaboration](#remove-a-collaboration)
- [Get a Collaboration's Information](#get-a-collaborations-information)
- [Get the Collaborations on a Folder](#get-the-collaborations-on-a-folder)
- [Get the Collaborations on a File](#get-the-collaborations-on-a-file)
- [Get Pending Collaborations](#get-pending-collaborations)
- [Accept or Decline a Pending Collaboration](#accept-or-decline-a-pending-collaboration)

Add a Collaboration
-------------------

You can add a collaboration on a folder by calling `add_collaborator(collaborator, role)`. The
`role` parameter determines what permissions the collaborator will have on the folder.

```python
folder_id = '1234'
collaborator = {'type': 'user', 'id': '1111'}
folder = client.folder(folder_id).get()
collaboration = folder.add_collaborator(collaborator, CollaborationRole.VIEWER)
```

Alternatively you can also invite a user with their email address.

```python
folder_id = '1234'
email_of_invitee = "testuser@example.com"
folder = client.folder(folder_id).get()
collaboration = folder.add_collaborator(email_of_invitee, CollaborationRole.VIEWER)
```

Edit a Collaboration
--------------------

A collaboration can be edited by using `update_info()`.

```python
collaboration_id = '1111'
collaboration_update = {'role': CollaborationRole.EDITOR}
collaboration = client.collaboration(collaboration_id)
updated_collaboration = collaboration.update_info(collaboration_update)
```

Remove a Collaboration
----------------------

A collaboration can be removed by calling `delete()`.

```python
collaboration_id = '1111'
collaboration = client.collaboration(collaboration_id).delete()
```

Get a Collaboration's Information
---------------------------------

To get information about a specific collaboration use `get()`.

```python
collaboration_id = '1111'
collaboration_info = client.collaboration(collaboration_id).get()
```

Get Collaborations on a Folder
------------------------------

To retrieve all collaborations on a specified folder you can use `collaborations()`.

```python
folder_id = '1234'
folder = client.folder(folder_id).get()
collaborations_on_folder = folder.collaborations()
first_collaboration = collaborations_on_folder.next()
```

Get Collaborations on a File
----------------------------

To retrieve an iterable of collaborations on a specified file you can use `collaborations()`.

```python
file_id = '2222'
file = client.file(file_id).get()
collaborations_on_file = folder.collaborations()
first_collaboration = collaborations_on_file.next()
```

Get Pending Collaborations on Folder
------------------------------------

To retrieve all pending collaborations on a folder use `pending_collaborations(status)`. The status is always set to `pending`.

```python
folder_id = '1234'
pending_collaborations_on_folder = client.folder(folder_id).pending_collaborations('pending')
```

Get Pending Collaborations on File
----------------------------------

To retrieve all pending collaborations on a file use `pending_collaborations(status)`. The status is always set to `pending`.

```python
file_id = '2222'
pending_collaborations_on_file = client.file(file_id).pending_collaborations('pending')
```

Accept or Decline a Pending Collaboration
-----------------------------------------

To `accept` or `reject` a pending collaboration use `respond_to_collaboration(new_status)`.

```python
new_status = 'accepted'
collaboration_id = '3333'
client.collaboration(collaboration_id).respond_to_collaboration(new_status)
```

Alternatively. you can reject a pending collaboration with

```python
new_status = 'rejected'
collaboration_id = '3333'
client.collaboration(collaboration_id).response_to_collaboration(new_status)
```
