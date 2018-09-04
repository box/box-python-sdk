Web Links
=========

Web links are objects that point to URLs. These objects are also known as
bookmarks within the Box web application. Web link objects are treated
similarly to file objects.

- [Create Web Link](#create-web-link)
- [Get Web Link](#get-web-link)
- [Update Web Link](#update-web-link)
- [Delete Web Link](#delete-web-link)

Create Web Link
---------------

Calling `create_web_link(target_url, name, description)` will let you create a new web link with a specified name and description.

```python
folder_id = '1234'
target_url = 'https://example.com'
link_name = 'Example Link'
link_description = 'This is the description'
folder = client.folder(folder_id).get()
web_link = folder.create_web_link(target_url, link_name, link_description)
```

Get Web Link
------------

Calling `get()` can be used to retrieve information regarding a specific weblink.

```python
web_link_id = '1234'
web_link = client.web_link(web_link_id).get()
```

Update Web Link
---------------

Calling `update()` can be used to update the weblink.

```python
web_link_update = {'url': 'https://newurl.com'}
updated_web_link = client.web_link.update_info(web_link_update)
```

Delete Web Link
---------------

Calling `delete()` can be used to delete a specified weblink.

```python
web_link_id = '1234'
client.web_link(web_link_id).delete()
```
