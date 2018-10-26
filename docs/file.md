Chunked Upload
--------------

For large files or in cases where the network connection is less reliable,
you may want to upload the file in parts.  This allows a single part to fail
without aborting the entire upload, and failed parts can then be retried.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Manual Process](#manual-process)
  - [Create Upload Session for File Version](#create-upload-session-for-file-version)
  - [Create Upload Session for File](#create-upload-session-for-file)
  - [Upload Part](#upload-part)
  - [Commit Upload Session](#commit-upload-session)
  - [Abort Upload Session](#abort-upload-session)
  - [List Upload Parts](#list-upload-parts)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

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
print('File ID: {0} and File Name: {1}'.format(uploaded_file.id, uploaded_file.name))
```

The individual endpoint methods are detailed below:

#### Create Upload Session for File Version

To create an upload session for uploading a large version, use `file.create_upload_session(file_size, file_name=None)`

```python
file_size = 26000000
upload_session = client.file('11111').create_upload_session(file_size=file_size)
```

#### Create Upload Session for File

To create an upload session for uploading a large file, use
`folder.create_upload_session(file_size, file_name)`

```python
file_size = 26000000
file_name = 'test_file.pdf'
upload_session = client.folder('22222').create_upload_session(file_size, file_name)
```

#### Upload Part

To upload a part of the file to this session, use `upload_session.upload_part(part_bytes, offset, total_size, part_content_sha1=None)`

```python
offset = 25165824
part_bytes = b'abcdefgh'
upload_session = client.upload_session('11493C07ED3EABB6E59874D3A1EF3581')
chunk = part_bytes.read(upload_session.part_size)
upload_part = upload_session.upload_part(chunk, offset, total_size)
```

#### Commit Upload Session

To commit the upload session to Box, use `upload_session.commit(content_sha1, parts=None, file_attributes=None, etag=None)`.

```python
import hashlib
parts = client.upload_session('11493C07ED3EABB6E59874D3A1EF3581').get_parts()
uploaded_file = client.upload_session('11493C07ED3EABB6E59874D3A1EF3581').commit(parts, sha1.digest())
```

#### Abort Upload Session

To abort a chunked upload, use `upload_session.abort()`.

```python
client.upload_session('11493C07ED3EABB6E59874D3A1EF3581').abort()
```

#### List Upload Parts

To return the list of parts uploaded so far, use `upload_session.get_parts(limit=None, offset=None)`.

```python
parts = client.upload_session('11493C07ED3EABB6E59874D3A1EF3581').get_parts()
```
