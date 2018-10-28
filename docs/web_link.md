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

Calling `folder.create_web_link(target_url, name=None, description=None)` will let you create a new web link with a specified name and description.

```python
folder_id = '1234'
target_url = 'https://example.com'
link_name = 'Example Link'
link_description = 'This is the description'
web_link = client.folder(folder_id).create_web_link(target_url, link_name, link_description)
```

Get Web Link
------------

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
