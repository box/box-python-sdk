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

For more complicated upload scenarios, such as those being coordinated across
multiple processes or when an unrecoverable error occurs with the automatic
uploader, the endpoints for chunked upload operations are also exposed directly.

The individual endpoint methods are detailed below:

#### Create Upload Session for File Version

To create an upload session for uploading a large version, use `file.create_upload_session(file_size, file_name=None)`

```python
file_size = 197520
upload_session = client.file('11111').create_upload_session(file_size=file_size)
```

#### Create Upload Session for File

To create an upload session for uploading a large file, use
`folder.create_upload_session(file_size, file_name)`

```python
file_size = 197520
file_name = 'test_file.pdf'
upload_session = client.folder('22222').create_upload_session(file_size=file_size, file_name=file_name)
```

#### Upload Part

To upload a part of the file to this session, use `upload_session.upload_part(part_bytes, offset, total_size, part_content_sha1=None)`

```python
from io import BytesIO
offset = 32
part_bytes = BytesIO(b'abcdefgh')
upload_session = client.upload_session('11493C07ED3EABB6E59874D3A1EF3581')
chunk = part_bytes.read(upload_session.part_size)
offset = 32
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

To return the list of parts uploaded so far, use `upload_session.get_parts(limit=None, offset=None, fields=None)`.

```python
parts = client.upload_session('11493C07ED3EABB6E59874D3A1EF3581').get_parts()
```