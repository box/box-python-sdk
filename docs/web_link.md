Web Links
=========

Web links are objects that point to URLs. These objects are also known as
bookmarks within the Box web application. Web link objects are treated
similarly to file objects.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Create Web Link](#create-web-link)
- [Get Web Link](#get-web-link)
- [Update Web Link](#update-web-link)
- [Delete Web Link](#delete-web-link)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Create Web Link
---------------

To create a web link object, first call `[client.folder(folder_id)]`[folder] to construct the appropriate ['Folder'][folder_class] object, and then calling [`folder.create_web_link(target_url, name=None, description=None)`][create] will let you create a new web link with a specified name and description. This method return an updated [`WebLink`][web_link_class] object populated with data from the API, leaving the original unmodified.

```python
web_link = client.folder('12345').create_web_link('https://example.com', 'Example Link', 'This is the description')
```

[folder]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.Folder
[folder_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder
[create]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder.create_web_link
[web_link_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.web_link.WebLink

Get Web Link
------------

To get a web link object, first call `[client.web_link(web_link_id)]`[web_link] to construct the appropriate [`WebLink`][web_link_class] object, and then calling []
Calling `web_link.get()` can be used to retrieve information regarding a specific weblink.

```python
web_link_id = '1234'
web_link = client.web_link(web_link_id).get()
```

Update Web Link
---------------

Calling `web_link.update_info()` can be used to update the weblink.

```python
web_link_update = {'url': 'https://newurl.com'}
updated_web_link = client.web_link.update_info(web_link_update)
```

Delete Web Link
---------------

Calling `web_link.delete()` can be used to delete a specified weblink.

```python
web_link_id = '1234'
client.web_link(web_link_id).delete()
```
