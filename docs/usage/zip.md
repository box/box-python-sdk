Zip
========

Allows you to create a temporary zip file on Box, containing Box files and folders, and then download it.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Download a Zip File](#download-a-zip-file)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Download a Zip File
-----------------------------

Calling [`client.download_zip(name, items, writable_stream)`][create_zip] will let you create a new zip file 
with the specified name and with the specified items and download it to the stream that is passed in. The response is a status `dict` that contains information about the download, including whether it was successful. The created zip file does not show up in your Box account.

```python
name = 'test'
file = mock_client.file('466239504569')
folder = mock_client.folder('466239504580')
items = [file, folder]
output_file = open('test.zip', 'wb')
status = client.download_zip(name, items, output_file)
print(f'The status of the zip download is {status["state"]}')
```

[download_zip]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.download_zip
