File Requests
=============

File request objects represent a file request associated with a folder.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Get a File Request's Information](#get-a-file-requests-information)
- [Copy a File Request's Information](#copy-a-file-requests-information)
- [Update a File Request's Information](#update-a-file-requests-information)
- [Delete a File Request](#delete-a-file-request)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Get a File Request's Information
------------------------

To get a file request object, first call [`client.file_request(file_request_id)`][file_request] to construct the appropriate [`FileRequest`][file_request_class] object, and then calling [`file_request.get(*, fields=None, headers=None, **kwargs)`][get] will return the [`FileRequest`][file_request_class] object populated with data 
from the API, leaving the original object unmodified.

<!-- sample get_file_requests_id -->
```python
file_request = client.file_request(file_request_id='123456').get()
print(f'File request {file_request.id} on folder {file_request.folder.name}')
```

[file_request]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.file_request
[file_request_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file_request.FileRequest
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get


Copy a File Request's Information
---------------------------

To copy a file request, first call [`client.file_request(file_request_id)`][file_request] to construct the appropriate [`FileRequest`][file_request_class] object, and then calling [`file_request.copy(folder, description=None, title=None, expires_at=None, require_description=None, require_email=None, status=None)`][copy]. It will return the [`FileRequest`][file_request_class] object populated with data new created file request from the API.

<!-- sample post_file_requests_id_copy -->
```python
file_request = client.file_request(file_request_id='123456')
folder = client.folder(folder_id='123456789')
new_file_request = file_request.copy(folder=folder, title="Copied file request")
```

[file_request_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file_request.FileRequest
[copy]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file_request.FileRequest.copy

Update a File Request's Information
---------------------------

To update a file request object, call [`file_request.update_info(data=file_request_update)`][update_info] with a `dict` of properties to
update on the file request. This method returns a newly updated [`FileRequest`][file_request_class] object, leaving the original object unmodified.

<!-- sample put_file_requests_id -->
```python
from boxsdk.object.file_request import StatusState
update_data = {
    "description": 'Updated description', 
    "is_email_required": True,
    "status": StatusState.ACTIVE
}
file_request.update_info(data=update_data)
```

[update_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.update_info
[file_request_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file_request.FileRequest

Delete a File Request
-------------

To delete a file request, call [`file_request.delete()`][delete], it deletes a file request permanently.

<!-- sample delete_file_requests_id -->
```python
file_request = client.file_request(file_request_id='123456')
file_request.delete()
```

[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.delete