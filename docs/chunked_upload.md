Chunked Upload
==============

This API provides a way to reliably upload large files to Box by chunking them into a sequence of parts. When using this API instead of the single file upload API, a request failure means a client only needs to retry upload of a single part instead of the entire file. Parts can also be uploaded in parallel allowing for potential performance improvement.

It is important to note that the Chunked Upload API is intended for large files with a minimum size of 20MB.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Create Upload Session for File Version](#create-upload-session-for-file-version)
- [Get Upload Session](#get-upload-session)
- [Create Upload Session for File](#create-upload-session-for-file)
- [Upload Part](#upload-part)
- [Commit](#commit)
- [List Uploaded Parts](#list-uploaded-parts)
- [Abort](#abort)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Create Upload Session for File Version
--------------------------------------

To create an upload session for uploading a large version, use `file.create_upload_session(file_size, file_name=None)`

```python
file_size = 197520
upload_session = client.file('11111').create_upload_session(file_size=file_size)
```

Get Upload Session
------------------

To get an upload session, use `upload_session.get()`.

```python
upload_session = client.upload_session('11493C07ED3EABB6E59874D3A1EF3581').get()
```

Create Upload Session for File
------------------------------

To create an upload session for uploading a large file, use
`folder.create_upload_session(file_size, file_name)`

```python
file_size = 197520
file_name = 'test_file.pdf'
upload_session = client.folder('22222').create_upload_session(file_size=file_size, file_name=file_name)
```

Upload Part
-----------

To upload a part of the file to this session, use `upload_session.upload_part(content_stream, offset, total_size, part_content_sha1=None)`

```python
from io import BytesIO
chunk = BytesIO(b'abcdefgh')
offset = 32
upload_part = client.upload_session('11493C07ED3EABB6E59874D3A1EF3581').upload_part(chunk, offset, total_size)
```

Commit
------

To commit the upload session to Box, use `upload_session.commit(parts, content_sha1)`.

```python
import hashlib
parts = client.upload_session('11493C07ED3EABB6E59874D3A1EF3581').get_parts()
uploaded_file = client.upload_session('11493C07ED3EABB6E59874D3A1EF3581').commit(parts, sha1.digest())
```

List Uploaded Parts
-------------------

To return the list of parts uploaded so far, use `upload_session.get_parts()`.

```python
parts = client.upload_session('11493C07ED3EABB6E59874D3A1EF3581').get_parts()
```

Abort
-----

To abort a chunked upload, use `upload_session.abort()`.

```python
client.upload_session('11493C07ED3EABB6E59874D3A1EF3581').abort()
```
