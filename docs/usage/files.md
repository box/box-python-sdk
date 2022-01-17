Files
=====

File objects represent individual files in Box. They can be used to download a
file's contents, upload new versions, and perform other common file operations
(move, copy, delete, etc.).

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Get a File's Information](#get-a-files-information)
- [Update a File's Information](#update-a-files-information)
- [Download a File](#download-a-file)
- [Get Download URL](#get-download-url)
- [Upload a File](#upload-a-file)
- [Chunked Upload](#chunked-upload)
  - [Automatic Uploader](#automatic-uploader)
    - [Resume Upload](#resume-upload)
    - [Abort Chunked Upload](#abort-chunked-upload)
  - [Manual Process](#manual-process)
    - [Create Upload Session for File Version](#create-upload-session-for-file-version)
    - [Create Upload Session for File](#create-upload-session-for-file)
    - [Upload Part](#upload-part)
    - [Commit Upload Session](#commit-upload-session)
    - [Abort Upload Session](#abort-upload-session)
    - [List Upload Parts](#list-upload-parts)
- [Move a File](#move-a-file)
- [Copy a File](#copy-a-file)
- [Rename a File](#rename-a-file)
- [Delete a File](#delete-a-file)
- [Get Previous Versions of a File](#get-previous-versions-of-a-file)
- [Upload a New Version of a File](#upload-a-new-version-of-a-file)
- [Promote a Previous Version of a File](#promote-a-previous-version-of-a-file)
- [Delete a Previous Version of a File](#delete-a-previous-version-of-a-file)
- [Lock a File](#lock-a-file)
- [Unlock a File](#unlock-a-file)
- [Create a Shared Link Download URL](#create-a-shared-link-download-url)
- [Find a File for a Shared Link](#find-a-file-for-a-shared-link)
- [Create a Shared Link](#create-a-shared-link)
- [Update a Shared Link](#update-a-shared-link)
- [Get a Shared Link](#get-a-shared-link)
- [Remove a Shared Link](#remove-a-shared-link)
- [Get an Embed Link](#get-an-embed-link)
- [Get File Representations](#get-file-representations)
- [Get Thumbnail (Deprecated)](#get-thumbnail-deprecated)
- [Get Thumbnail](#get-thumbnail)
- [Set Metadata](#set-metadata)
- [Get Metadata](#get-metadata)
- [Remove Metadata](#remove-metadata)
- [Get All Metadata](#get-all-metadata)
- [Set a Classification](#set-a-classification)
- [Retrieve a Classification](#retrieve-a-classification)
- [Remove a Classification](#remove-a-classification)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Get a File's Information
------------------------

Calling [`file.get(*, fields=None, etag=None, **kwargs)`][get_info] on a [`File`][file_class] retrieves information
about the file from the API. This method returns a new [`File`][file_class] object populated with the information retrieved. 

You can specify an `Iterable` of fields to retrieve from the API in the `fields` parameter.

<!-- sample get_files_id -->
```python
file_id = '11111'
file_info = client.file(file_id).get()
print(f'File "{file_info.name}" has a size of {file_info.size} bytes')
```

[get_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get
[file_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File

Update a File's Information
---------------------------

To update fields on the [`File`][file_class] object, call [`file.update_info(data=data_to_update)`][update_info] with
a `dict` of fields to update.  This method returns the updated [`File`][file_class] object, leaving the original it
was called on unmodified.

<!-- sample put_files_id -->
```python
file_id = '11111'
updated_file = client.file(file_id).update_info(data={'description': 'My file'})
```

Download a File
---------------

A file can be downloaded in two ways: by returning the entire contents of the file as `bytes` or by providing an output
stream to which the contents of the file will be written.  For both methods, you can optionally download a specific
version of the file by passing the desired [`FileVersion`][file_version_class] in the `file_version` parameter.  You may
also wish to download only a certain chunk of the file by passing a tuple of byte offsets via the `byte_range`
parameter — the lower and upper bounds you wish to download.

To get the entire contents of the file as `bytes`, call [`file.content(file_version=None, byte_range=None)`][content]. 

<!-- sample get_files_id_content -->
```python
file_id = '11111'
file_content = client.file(file_id).content()
```

For users with premium accounts, previous versions of a file can be downloaded.

<!-- sample get_files_id_content for_version -->
```python
file_id = '11111'
file_version = client.file_version('12345')
version_content = client.file(file_id).content(file_version=file_version)
```

Additonally, only a part of the file can be downloaded by specifying a byte range.

```python
file_id = '11111'
beginning_of_file_content = client.file(file_id).content(byte_range=(0,99))
```

To download the file contents to an output stream, call
[`file.download_to(writeable_stream, file_version=None, byte_range=None)`][download_to] with the stream.

```python
file_id = '11111'

# Write the Box file contents to disk
output_file = open('file.pdf', 'wb')
client.file(file_id).download_to(output_file)
```

[file_version_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file_version.FileVersion
[content]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.content
[download_to]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.download_to

Get Download URL
----------------

To get a download URL suitable for passing to a web browser or other application, which will allow someone to download
the file, call [`file.get_download_url(file_version=None)`][get_download_url].  The will return a `unicode` string
containing the file's download URL.  You can optionally pass a [`FileVersion`][file_version_class] via the
`file_version` parameter to get a download URL for a specific version of the file.

<!-- sample get_files_id_content get_url -->
```python
file_id = '11111'
download_url = client.file(file_id).get_download_url()
print(f'The file\'s download URL is: {download_url}')
```

[get_download_url]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.get_download_url

Upload a File
-------------

Files are uploaded to a folder in one of two ways: by providing a path to a file on disk, or via a readable stream
containing the file contents.

To upload a file from a path on disk, call the
[`folder.upload(file_path, file_name=None, file_description=None,preflight_check=False, preflight_expected_size=0)`][upload] method
on the [`Folder`][folder_class] you want to upload the file into.  By default, the file uploaded to Box will have the
same file name as the one on disk; you can override this by passing a different name in the `file_name` parameter. You can, optionally, also choose to set a file description upon upload by using the `file_description` parameter.
This method returns a [`File`][file_class] object representing the newly-uploaded file.

<!-- sample post_files_content -->
```python
folder_id = '22222'
new_file = client.folder(folder_id).upload('/home/me/document.pdf')
print(f'File "{new_file.name}" uploaded to Box with file ID {new_file.id}')
```

To upload a file from a readable stream, call
[`folder.upload_stream(file_stream, file_name, file_description=None, preflight_check=False, preflight_expected_size=0)`][upload_stream]
with the stream and a name for the file.  This method returns a [`File`][file_class] object representing the
newly-uploaded file.

```python
file_name = 'file.pdf'
stream = open('/path/to/file.pdf', 'rb')

folder_id = '22222'
new_file = client.folder(folder_id).upload_stream(stream, file_name)
print(f'File "{new_file.name}" uploaded to Box with file ID {new_file.id}')
```

[folder_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder
[upload]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder.upload
[upload_stream]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder.upload_stream

Chunked Upload
--------------

For large files or in cases where the network connection is less reliable,
you may want to upload the file in parts.  This allows a single part to fail
without aborting the entire upload, and failed parts can then be retried.

### Automatic Uploader

The SDK provides a method of automatically handling a chunked upload; simply call [`chunked_upload.start()`][start] 
with the path to the file you wish to upload from the [`File`][file_class] with 
[`file.get_chunked_uploader(file_path, rename_file=False)`][get_chunked_uploader_for_version] method to retrieve a 
[`ChunkedUploader`][chunked_uploader_class] object for a new 
version upload or from the [`Folder`][folder_class] with [`folder.get_chunked_uploader(file_path)`][get_chunked_uploader_for_file] 
method to retrieve a [`ChunkedUploader`][chunked_uploader_class] object for a new file upload. You can also return a 
[`ChunkedUploader`][chunked_uploader_class] object by creating a [`UploadSession`][upload_session_class] object first 
and calling the method, [`upload_session.get_chunked_upload(file_path)`][get_chunked_uploader] or 
[`upload_session.get_chunked_uploader_for_stream(content_stream, file_size)`][get_chunked_uploader_for_stream].
Calling the method [`chunked_upload.start()`][start] will kick off the chunked upload process and return the [File][file_class] 
object that was uploaded.

<!-- samples x_chunked_uploads automatic -->
```python
chunked_uploader = client.file('12345').get_chunked_uploader('/path/to/file')
uploaded_file = chunked_uploader.start()
print(f'File "{uploaded_file.name}" uploaded to Box with file ID {uploaded_file.id}')
```

Alternatively, you can create an upload session and calling [`upload_session.get_chunked_uploader(file_path)`][get_chunked_uploader] 
or [`upload_session.get_chunked_uploader_for_stream(content_stream, file_size)`][get_chunked_uploader_for_stream].

```python
chunked_uploader = client.upload_session('56781').get_chunked_uploader('/path/to/file')
uploaded_file = chunked_uploader.start()
print(f'File "{uploaded_file.name}" uploaded to Box with file ID {uploaded_file.id}')
```

```python
test_file_path = '/path/to/large_file.mp4'
content_stream = open(test_file_path, 'rb')
total_size = os.stat(test_file_path).st_size
chunked_uploader = client.upload_session('56781').get_chunked_uploader_for_stream(content_stream, total_size)
uploaded_file = chunked_uploader.start()
print(f'File "{uploaded_file.name}" uploaded to Box with file ID {uploaded_file.id}')
```

[start]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.chunked_uploader.ChunkedUploader.start
[chunked_uploader_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.chunked_uploader.ChunkedUploader
[get_chunked_uploader_for_version]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.get_chunked_uploader
[get_chunked_uploader_for_file]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder.get_chunked_uploader
[upload_session_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.upload_session.UploadSession
[get_chunked_uploader]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.upload_session.UploadSession.get_chunked_uploader
[get_chunked_uploader_for_stream]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.upload_session.UploadSession.get_chunked_uploader_for_stream

#### Resume Upload

Sometimes an upload can be interrupted, in order to resume uploading where you last left off, simply call the
[`chunked_uploader.resume()`][resume] method. This will return the the [File][file_class] object that was uploaded.

```python
chunked_uploader = client.file('12345').get_chunked_uploader('/path/to/file')
try:
    uploaded_file = chunked_uploader.start()
except:
    uploaded_file = chunked_uploader.resume()
print(f'File "{uploaded_file.name}" uploaded to Box with file ID {uploaded_file.id}')
```

Alternatively, you can also create a [`UploadSession`][upload_session_class] object by calling
[`client.upload_session(session_id)`][upload_session] if you have the upload session id. This can be helpful in 
resuming an existing upload session.


```python
chunked_uploader = client.upload_session('12345').get_chunked_uploader('/path/to/file')
uploaded_file = chunked_uploader.resume()
print(f'File "{uploaded_file.name}" uploaded to Box with file ID {uploaded_file.id}')
```

[resume]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.chunked_uploader.ChunkedUploader.resume

#### Abort Chunked Upload

To abort a running upload, which cancels all currently uploading chunks and aborts the upload session, call the method
[`chunked_uploader.abort()`][abort].

```python
from boxsdk.exception import BoxNetworkException

test_file_path = '/path/to/large_file.mp4'
content_stream = open(test_file_path, 'rb')
total_size = os.stat(test_file_path).st_size
chunked_uploader = client.upload_session('56781').get_chunked_uploader_for_stream(content_stream, total_size)
try:
    uploaded_file = chunked_uploader.start()
except BoxNetworkException:
    chunked_uploader.abort()
```

### Manual Process

For more complicated upload scenarios, such as those being coordinated across multiple processes or when an unrecoverable error occurs with the automatic uploader, the endpoints for chunked upload operations are also exposed directly.

For example, this is roughly how a chunked upload is done manually:

```python
import hashlib
import os


test_file_path = '/path/to/large_file.mp4'
total_size = os.stat(test_file_path).st_size
sha1 = hashlib.sha1()
content_stream = open(test_file_path, 'rb')
upload_session = client.folder(folder_id='11111').create_upload_session(file_size=total_size, file_name='test_file_name.mp4')
part_array = []

for part_num in range(upload_session.total_parts):

    copied_length = 0
    chunk = b''
    while copied_length < upload_session.part_size:
        bytes_read = content_stream.read(upload_session.part_size - copied_length)
        if bytes_read is None:
            # stream returns none when no bytes are ready currently but there are
            # potentially more bytes in the stream to be read.
            continue
        if len(bytes_read) == 0:
            # stream is exhausted.
            break
        chunk += bytes_read
        copied_length += len(bytes_read)

    uploaded_part = upload_session.upload_part_bytes(chunk, part_num*upload_session.part_size, total_size)
    part_array.append(uploaded_part)
    updated_sha1 = sha1.update(chunk)
content_sha1 = sha1.digest()
uploaded_file = upload_session.commit(content_sha1=content_sha1, parts=part_array)
print(f'File ID: {uploaded_file.id} and File Name: {uploaded_file.name}')
```

The individual endpoint methods are detailed below:

#### Create Upload Session for File Version

To create an upload session for uploading a large version, call
[`file.create_upload_session(file_size, file_name=None)`][create_version_upload_session] with the size of the file to be
uploaded.  You can optionally specify a new `file_name` to rename the file on upload.  This method returns an
[`UploadSession`][upload_session_class] object representing the created upload session.

<!-- sample post_files_id_upload_sessions -->
```python
file_size = 26000000
upload_session = client.file('11111').create_upload_session(file_size)
print(f'Created upload session {upload_session.id} with chunk size of {upload_session.part_size} bytes')
```

[create_version_upload_session]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.create_upload_session
[upload_session_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.upload_session.UploadSession

#### Create Upload Session for File

To create an upload session for uploading a new large file, call
[`folder.create_upload_session(file_size, file_name)`][create_upload_session] with the size and filename of the file
to be uploaded.  This method returns an [`UploadSession`][upload_session_class] object representing the created upload
session.

<!-- sample post_files_upload_sessions -->
```python
file_size = 26000000
file_name = 'test_file.pdf'
upload_session = client.folder('22222').create_upload_session(file_size, file_name)
print(f'Created upload session {upload_session.id} with chunk size of {upload_session.part_size} bytes')
```

[create_upload_session]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder.create_upload_session

#### Upload Part

To upload a part of the file to this session, call
[`upload_session.upload_part_bytes(part_bytes, offset, total_size, part_content_sha1=None)`][upload_part_bytes] with
the `bytes` to be uploaded, the byte offset within the file (which should be a multiple of the upload session
`part_size`), and the total size of the file being uploaded.  This method returns a `dict` for the part record; these
records should be kept for the commit operation.

> __Note:__ The number of bytes uploaded for each part must be exactly `upload_sesion.part_size`, except for the last
> part (which just includes however many bytes are left in the file).

<!-- sample put_files_upload_sessions_id -->
```python
upload_session = client.upload_session('11493C07ED3EABB6E59874D3A1EF3581')
offset = upload_session.part_size * 3
total_size = 26000000
part_bytes = b'abcdefgh'
part = upload_session.upload_part_bytes(part_bytes, offset, total_size)
print(f'Successfully uploaded part ID {part["part_id"]}')
```

[upload_part_bytes]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.upload_session.UploadSession.upload_part_bytes

#### Commit Upload Session

After uploading all parts of the file, commit the upload session to Box by calling
[`upload_session.commit(content_sha1, parts=None, file_attributes=None, etag=None)`][commit] with the SHA1 hash of the
entire file.  For best consistency guarantees, you should also pass an `Iterable` of the parts `dict`s via the `parts`
parameter; otherwise, the list of parts will be retrieved from the API.  You may also pass a `dict` of `file_attributes`
to set on the new file.

<!-- sample post_files_upload_sessions_id_commit -->
```python
import hashlib

sha1 = hashlib.sha1()
# sha1 should have been updated with all the bytes of the file

file_atributes = {
    'description': 'A file uploaded via Chunked Upload',
}

upload_session = client.upload_session('11493C07ED3EABB6E59874D3A1EF3581')
uploaded_file = upload_session.commit(sha1.digest(), file_atributes=file_atributes)
print(f'Successfully uploaded file {uploaded_file.id} with description {uploaded_file.description}')
```

[commit]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.upload_session.UploadSession.commit

#### Abort Upload Session

To abort a chunked upload and lose all uploaded file parts, call [`upload_session.abort()`][abort].  This method returns
`True` to indicate that the deletion succeeded.

<!-- sample delete_files_upload_sessions_id -->
```python
client.upload_session('11493C07ED3EABB6E59874D3A1EF3581').abort()
print('Upload was successfully canceled')
```

[abort]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.upload_session.UploadSession.abort

#### List Upload Parts

To return the list of parts uploaded so far, call [`upload_session.get_parts(limit=None, offset=None)`][get_parts].
This method returns a `BoxObjectCollection` that allows you to iterate over the part `dict`s in the collection.

<!-- sample get_files_upload_sessions_id_parts -->
```python
parts = client.upload_session('11493C07ED3EABB6E59874D3A1EF3581').get_parts()
for part in parts:
    print(f'Part {part["part_id"]} at offset {part["offset"]} has already been uploaded')
```

[get_parts]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.upload_session.UploadSession.get_parts

Move a File
-----------

To move a file from one folder into another, call [`file.move(parent_folder, name=None)`][move] with the destination
folder to move the file into.  You can optionally provide a `name` parameter to automatically rename the file in case
of a name conflict in the destination folder.  This method returns the updated [`File`][file_class] object in the new
folder.

```python
file_id = '11111'
destination_folder_id = '44444'

file_to_move = client.file(file_id)
destination_folder = client.folder(destination_folder_id)

moved_file = file_to_move.move(destination_folder)
print(f'File "{moved_file.name}" has been moved into folder "{moved_file.parent.name}"')
```

[move]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_item.BaseItem.move

Copy a File
-----------

A file can be copied to a new folder by calling [`file.copy(*, parent_folder, name=None, file_version=None, **_kwargs)`][copy]
with the destination folder and an optional new name for the file in case there is a name conflict in the destination
folder.  This method returns a [`File`][file_class] object representing the copy of the file in the destination folder.

<!-- sample post_files_id_copy -->
```python
file_id = '11111'
destination_folder_id = '44444'

file_to_copy = client.file(file_id)
destination_folder = client.folder(destination_folder_id)

file_copy = file_to_copy.copy(parent_folder=destination_folder)
print(f'File "{file_copy.name}" has been copied into folder "{file_copy.parent.name}"')
```

[copy]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_item.BaseItem.copy

Rename a File
-----------

A file can be renamed by calling [`file.rename(name)`][rename]. This method returns the updated
[`File`][file_class] object with a new name. Remeber to provide also extention of the file along with the new name. 

```python
file = client.file(file_id='11111')

renamed_file = file.rename("new-name.pdf")
print(f'File was renamed to "{renamed_file.name}"')
```

[rename]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_item.BaseItem.rename

Delete a File
-------------

Calling the [`file.delete()`][delete] method will delete the file.  Depending on enterprise settings, this will either move
the file to the user's trash or permanently delete the file.  This method returns `True` to signify that the deletion
was successful.

<!-- sample delete_files_id -->
```python
client.file(file_id='11111').delete()
```

[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.delete

Get Previous Versions of a File
-------------------------------

Previous versions of a file can be retrieved with the
[`file.get_previous_versions(limit=None, offset=None, fields=None)`][get_previous_versions] method.  This method returns
a [`BoxObjectCollection`][box_object_collection] that can iterate over the [`FileVersion`][file_version_class] objects
in the collection.

<!-- sample get_files_id_versions -->
```python
file_id = '11111'

file_versions = client.file(file_id).get_previous_versions()
for version in file_versions:
    print(f'File version {version.id} was created at {version.created_at}')
```

[get_previous_versions]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.get_previous_versions
[box_object_collection]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.pagination.html#boxsdk.pagination.box_object_collection.BoxObjectCollection

Upload a New Version of a File
------------------------------

New versions of a file can be uploaded in one of two ways: by providing a path to a file on disk, or via a readable
stream containing the file contents.

To upload a new file version from a path on disk, call the
[`file.update_contents(file_path, etag=None, preflight_check=False, preflight_expected_size=0)`][update_contents]
method.  This method returns a [`File`][file_class] object representing the updated file.

<!-- sample post_files_id_content -->
```python
file_id = '11111'
file_path = '/path/to/file.pdf'

updated_file = client.file(file_id).update_contents(file_path)
print(f'File "{updated_file.name}" has been updated')
```

To upload a file version from a readable stream, call
[`file.update_contents_with_stream(file_stream, etag=None, preflight_check=False, preflight_expected_size=0)`][update_contents_with_stream]
with the stream.  This method returns a [`File`][file_class] object representing the
newly-uploaded file.

```python
file_id = '11111'
stream = open('/path/to/file.pdf', 'rb')

updated_file = client.file(file_id).update_contents_with_stream(stream)
print(f'File "{updated_file.name}" has been updated')
```

[update_contents]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.update_contents
[update_contents_with_stream]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.update_contents_with_stream

Promote a Previous Version of a File
------------------------------------

A previous version of a file can be promoted by calling the [`file.promote_version(file_version)`][promote_version]
method to become the current version of the file with the [`FileVersion`][file_version_class] to promote.  This create a
copy of the old file version and puts it on the top of the versions stack.  This method returns the new copy
[`FileVersion`][file_version_class] object.

<!-- sample post_files_id_versions_current -->
```python
file_id = '11111'
file_version_id = '12345'

version_to_promote = client.file_version(file_version_id)

new_version = client.file(file_id).promote_version(version_to_promote)
print(f'Version {file_version_id} promoted; new version {new_version.id} created')
```

[promote_version]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.promote_version

Delete a Previous Version of a File
-----------------------------------

A version of a file can be deleted and moved to the trash by calling
[`file.delete_version(file_version, etag=None)`][delete_version] with the [`FileVersion`] to delete.

<!-- sample delete_files_id_versions_id -->
```python
file_id = '11111'
version_id = '12345'

version_to_delete = client.file_version(version_id)
client.file(file_id).delete_version(version_to_delete)
```

[delete_version]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.delete_version

Lock a File
-----------

A locked file cannot be modified by any other user until it is unlocked.  This is useful if you want to "check out" a
file while you're working on it, to ensure that other collaborators do not make changes while your changes are in
progress.

To lock a file, call [`file.lock(prevent_download=False, expire_time=None)`][lock].  You can optionally prevent other
users from downloading the file while it is locked by passing `True` for the `prevent_download` parameter.  You can also
set an expiration time for the lock, which will automatically release the lock at the specified time.  The expiration
time is formatted as an [RFC3339 datetime][rfc3339].

This method returns the updated [`File`][file_class] object.

```python
file_id = '11111'

updated_file = client.file(file_id).lock(expiration_time='2020-01-01T00:00:00-08:00')
print(f'File "{updated_file.name}" has been locked!')
```

[lock]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.lock
[rfc3339]: https://tools.ietf.org/html/rfc3339#section-5.8

Unlock a File
-------------

A locked file can be unlocked by calling [`file.unlock()`][unlock].  This method returns the updated
[`File`][file_class] object.

```python
file_id = '11111'

updated_file = client.file(file_id).unlock()
print(f'File "{updated_file.name}" has been unlocked!')
```

[unlock]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.unlock

Create a Shared Link Download URL
--------------------

A shared link for a file can be generated by calling
[`file.get_shared_link_download_url(access=None, etag=None, unshared_at=None, allow_preview=None, password=None, vanity_name=None)`][get_shared_link_download_url].
This method returns a `unicode` string containing the shared link URL.

<!-- sample put_files_id add_shared_link -->
```python
file_id = '11111'

url = client.file(file_id).get_shared_link_download_url(access='collaborators', vanity_name="my-unique-vanity-name")
print(f'The file shared link download URL is: {url}')
```

[get_shared_link_download_url]:
https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.get_shared_link_download_url

Find a File for a Shared Link
-----------------------------

To find a file given a shared link, use the
[`client.get_shared_item`](https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html?highlight=get_shared_item#boxsdk.client.client.Client.get_shared_item)
method.

<!-- sample get_shared_items -->
```python
file = client.get_shared_item('https://app.box.com/s/gjasdasjhasd', password='letmein')
```

Create a Shared Link
--------------------

A shared link for a file can be generated by calling
[`file.get_shared_link(*, access=None, etag=None, unshared_at=None, allow_download=None, allow_preview=None,
password=None, vanity_name=None, **kwargs)`][get_shared_link].
This method returns a `unicode` string containing the shared link URL.

<!-- sample put_files_id add_shared_link -->
```python
file_id = '11111'

url = client.file(file_id).get_shared_link(access='open', allow_download=False)
print(f'The file shared link URL is: {url}')
```

[get_shared_link]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.get_shared_link

Update a Shared Link
--------------------

A shared link for a file can be updated by calling
[`file.get_shared_link(*, access=None, etag=None, unshared_at=None, allow_download=None, allow_preview=None,
password=None, vanity_name=None, **kwargs)`][update_shared_link]
with an updated list of properties.

This method returns a `unicode` string containing the shared link URL.

<!-- sample put_files_id update_shared_link -->
```python
file_id = '11111'

url = client.file(file_id).get_shared_link(access='open', allow_download=True)
print(f'The file shared link URL is: {url}')
```

[update_shared_link]:
https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.get_shared_link

Get a Shared Link
--------------------

To check for an existing shared link on a file, simply call 
`file.shared_link`

This method returns a `unicode` string containing the shared link URL.

<!-- sample get_files_id get_shared_link -->
```python
file_id = '11111'
shared_link = client.file(file_id).get().shared_link
url = shared_link['url']
```

Remove a Shared Link
--------------------

A shared link for a file can be removed by calling [`file.remove_shared_link(*, etag=None, **kwargs)`][remove_shared_link].

<!-- sample put_files_id remove_shared_link -->
```python
file_id = '11111'
client.file(file_id).remove_shared_link()
```

[remove_shared_link]:
https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.remove_shared_link


Get an Embed Link
-----------------

A file embed URL can be generated by calling [`file.get_embed_url()`][get_embed_url].  This method returns a `unicode`
string containing a URL suitable for embedding in an `<iframe>` to embed the a file viewer in a web page.

```python
file_id = '11111'

embed_url = client.file(file_id).get_embed_url()
print(f'<iframe src="{embed_url}"></iframe>')
```

[get_embed_url]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.get_embed_url

Get File Representations
------------------------

To get the preview representations of a file, call the
[`file.get_representation_info(rep_hints=None)`][get_representation_info] method with the
[representation hints][rep_hints] to fetch — if no hints are provided, limited information about all available
representations will be returned.  This method returns a `list` of `dict`s containing the information about the
requested [representations][rep_api_obj].

Note that this method only provides information about a set of available representations; your
application will need to handle checking the status of the representations and downlaoding them
via the provided content URL template.

```python
file_id = '11111'
rep_hints = '[pdf][extracted_text]'

representations = client.file(file_id).get_representation_info(rep_hints)
for rep in representations:
    print(f'{rep["representation"]} representation has status {rep["status"]["state"]}')
    print(f'Info URL for this representation is: {rep["info"]["url"]}')
    print(f'Content URL template is: {rep["content"]["url_template"]}')
```

[get_representation_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.get_representation_info
[rep_hints]: https://developer.box.com/en/reference/get-files-id/#param-X-Rep-Hints
[rep_api_obj]: https://developer.box.com/en/reference/resources/representations

Get Thumbnail (Deprecated)
--------------------------

A thumbnail for a file can be retrieved by calling
[`file.get_thumbnail(extension='png', min_width=None, min_height=None, max_width=None, max_height=None)`][get_thumbnail].
This method returns the `bytes` of the thumbnail image.

<!-- sample get_files_id_thumbnail_id -->
```python
file_id = '11111'

thumbnail = client.file(file_id).get_thumbnail(extension='jpg') 
```

[get_thumbnail]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.get_thumbnail

Get Thumbnail
-------------

A thumbnail for a file can now be retrieved by calling [`file.get_thumbnail_representation(dimensions, extension='png')`][get_thumbnail_representation]. This method returns the `bytes` of the thumbnail image. You must pass in a dimension that is valid for the extension you pass in for this file. To find valid dimensions, you must first make a call with [`file.get_representation_info(rep_hints=None)`]. This will return a `dict` of all available representations with their extensions and dimensions. More details about can be found on our developer docs [here](https://developer.box.com/guides/representations/list-all-representations/). 

<!-- sample get_files_id_thumbnail_id -->
```python
file_id = '11111'

thumbnail = client.file(file_id).get_thumbnail_representation('92x92', extension='jpg') 
```

[get_thumbnail_representation]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.get_thumbnail_representation

Set Metadata
------------

To set metadata on a file call the [`file.metadata(scope='global', template='properties')`][metadata]
to specify the scope and template key of the metadata template to attach. Then, call the [`metadata.set(data)`][metadata_set] method with the key/value pairs to attach. This method returns a `dict` containing the applied metadata instance.

Note: This method will unconditionally apply the provided metadata, overwriting the existing metadata for the keys provided.
To specifically create or update metadata, see the `create()` or `update()` methods.

```python
metadata = {
    'foo': 'bar',
}
applied_metadata = client.file(file_id='11111').metadata(scope='enterprise', template='testtemplate').set(metadata)
print(f'Set metadata in instance ID {applied_metadata["$id"]}')
```

Metadata can be added to a file either as free-form key/value pairs or from an existing template.  To add metadata to
a file, first call [`file.metadata(scope='global', template='properties')`][metadata] to specify the scope and
template key of the metadata template to attach (or use the default values to attach free-form keys and values).  Then,
call [`metadata.create(data)`][metadata_create] with the key/value pairs to attach.  This method can only be used to
attach a given metadata template to the file for the first time, and returns a `dict` containing the applied metadata
instance.

Note: This method will only succeed if the provided metadata template is not currently applied to the file, otherwise it will 
fail with a Conflict error.

<!-- sample post_files_id_metadata_id_id -->
```python
metadata = {
    'foo': 'bar',
    'baz': 'quux',
}

applied_metadata = client.file(file_id='11111').metadata().create(metadata)
print(f'Applied metadata in instance ID {applied_metadata["$id"]}')
```

Updating metadata values is performed via a series of discrete operations, which are applied atomically against the
existing file metadata.  First, specify which metadata will be updated by calling
[`file.metadata(scope='global', template='properties')`][metadata].  Then, start an update sequence by calling
[`metadata.start_update()`][metadata_start_update] and add update operations to the returned
[`MetadataUpdate`][metadata_update_obj].  Finally, perform the update by calling
[`metadata.update(metadata_update)`][metadata_update].  This final method returns a `dict` of the updated metadata
instance.

Note: This method will only succeed if the provided metadata template has already been applied to the file; If the file does not
have existing metadata, this method will fail with a Not Found error. This is useful you know the file will already have metadata applied,
since it will save an API call compared to `set()`.

<!-- sample put_files_id_metadata_id_id -->
```python
file_obj = client.file(file_id='11111')
file_metadata = file_obj.metadata(scope='enterprise', template='myMetadata')

updates = file_metadata.start_update()
updates.add('/foo', 'bar')
updates.update('/baz', 'murp', old_value='quux')  # Ensure the old value was "quux" before updating to "murp"

updated_metadata = file_metadata.update(updates)
print('Updated metadata on file!')
print(f'foo is now {updated_metadata["foo"]} and baz is now {updated_metadata["baz"]}')
```

[set_metadata]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata.Metadata.set
[metadata]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.metadata
[metadata_create]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata.Metadata.create
[metadata_start_update]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata.Metadata.start_update
[metadata_update_obj]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata.MetadataUpdate
[metadata_update]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata.Metadata.update

Get Metadata
------------

To retrieve the metadata instance on a file for a specific metadata template, first call
[`file.metadata(scope='global', template='properties')`][metadata] to specify the scope and template key of the
metadata template to retrieve, then call [`metadata.get()`][metadata_get] to retrieve the metadata values attached to
the file.  This method returns a `dict` containing the applied metadata instance.

<!-- sample get_files_id_metadata_id_id -->
```python
metadata = client.file(file_id='11111').metadata(scope='enterprise', template='myMetadata').get()
print(f'Got metadata instance {metadata["$id"]}')
```

[metadata_get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata.Metadata.get

Remove Metadata
---------------

To remove a metadata instance from a file, call
[`file.metadata(scope='global', template='properties')`][metadata] to specify the scope and template key of the
metadata template to remove, then call [`metadata.delete()`][metadata_delete] to remove the metadata from the file.
This method returns `True` to indicate that the removal succeeded.

<!-- sample delete_files_id_metadata_id_id -->
```python
client.file(file_id='11111').metadata(scope='enterprise', template='myMetadata').delete()
```

[metadata_delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.metadata.Metadata.delete

Get All Metadata
----------------

To retrieve all metadata attached to a file, call [`file.get_all_metadata()`][get_all_metadata].  This method returns a
[`BoxObjectCollection`][box_object_collection] that can be used to iterate over the `dict`s representing each metadata 
instance attached to the
file.

<!-- sample get_files_id_metadata -->
```python
file_metadata = client.file(file_id='11111').get_all_metadata()
for instance in file_metadata:
    if 'foo' in instance:
        print(f'Metadata instance {instance["id"]} has value "{instance["foo"]}" for foo')
```

[get_all_metadata]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.get_all_metadata

Set a Classification
--------------------

It is important to note that this feature is only available if you have Governance.

To add classification to a [`File`][file_class], call [`file.set_classification(classification)`][set_classification].
This method returns the classification type on the [`File`][file_class] object. If a classification already exists then 
this call will update the existing classification with the new [`ClassificationType`][classification_type_class].

```python
from boxsdk.object.item import ClassificationType

classification = client.file(file_id='11111').set_classification(ClassificationType.PUBLIC)
print(f'Classification Type is: {classification}')
```

The set method will always work no matter the state your [`File`][file_class] is in. For cases already where a
classification value already exists [`set_classification(classification)`][set_classification] may make multiple 
API calls. 

Alternatively, if you already know you have a classification and you are simple updating it, you can use the 
[`update_classification(classification)`][update_classification]. This will ultimately help you save one extra API call.

```python
classification = client.file(file_id='11111').update_classification(ClassificationType.NONE)
print(f'Classification Type is: {classification}')
```

[set_classification]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.set_classification
[update_classification]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.update_classification
[classification_type_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.ClassificationType

Retrieve a Classification
-------------------------

To retrieve a classification from a [`File`][file_class], call [`file.get_classification()`][get_classification].
This method returns the classification type on the [`File`][file_class] object.

```python
classification = client.file(file_id='11111').get_classification()
print(f'Classification Type is: {classification}')
```

[get_classification]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.get_classification

Remove a Classification
-----------------------

To remove a classification from a [`File`][file_class], call [`file.remove_classification()`][remove_classification].

```python
client.file(file_id='11111').remove_classification()
```

[remove_classification]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.item.Item.remove_classification
