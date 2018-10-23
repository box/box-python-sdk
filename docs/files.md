Files
=====

File objects represent individual files in Box. They can be used to download a
file's contents, upload new versions, and perform other common file operations
(move, copy, delete, etc.).

Get a File's Information
------------------------

Calling [`file.get(fields=None)`][get_info] on a [`File`][file_class] retrieves information about the file from the API.
This method returns a new [`File`][file_class] object populated with the information retrieved. 

You can specify an `Iterable` of fields to retrieve from the API in the `fields` parameter.

```python
file_id = '11111'
file_info = client.file(file_id).get()
print('File "{0}" has a size of {1} bytes'.format(file_info.name, file_info.size))
```

[get_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get
[file_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File

Update a File's Information
---------------------------

To update fields on the [`File`][file_class] object, call [`file.update_info(data)`][update_info] with a `dict` of
fields to update.  This method returns the updated [`File`][file_class] object, leaving the original it was called on
unmodified.

```python
file_id = '11111'
updated_file = client.file(file_id).update_info({'description': 'My file'})
```

Download a File
---------------

A file can be downloaded in two ways: by returning the entire contents of the file as `bytes` or by providing an output
stream to which the contents of the file will be written.  For both methods, you can optionally download a specific
version of the file by passing the desired [`FileVersion`][file_version_class] in the `file_version` parameter.  You may
also wish to download only a certain chunk of the file by passing a tuple of byte offsets via the `byte_range`
parameter — the lower and upper bounds you wish to download.

To get the entire contents of the file as `bytes`, call [`file.content(file_version=None, byte_range=None)`][content].

```python
file_id = '11111'

# Download the entire file into memory
file_content = client.file(file_id).content()

# Download a specific file verison
file_version = client.file_version('12345')
version_content = client.file(file_id).content(file_version=file_version)

# Download the first 100 bytes of the file
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

```python
file_id = '11111'
download_url = client.file(file_id).get_download_url()
print('The file\'s download URL is: {0}'.format(download_url))
```

[get_download_url]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.get_download_url

Upload a File
-------------

Files are uploaded to a folder in one of two ways: by providing a path to a file on disk, or via a readable stream
containing the file contents.

To upload a file from a path on disk, call the [`folder.upload()`][upload] method
on the [`Folder`][folder_class] you want to upload the file into.
