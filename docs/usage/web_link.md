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

To create a web link object, calling [`folder.create_web_link(target_url, name=None, description=None)`][create] 
will let you create a new web link with a specified name and description. This method return an newly created [`WebLink`][web_link_class] 
object populated with data from the API, leaving the original object unmodified.

<!-- sample post_web_links -->
```python
web_link = client.folder(folder_id='12345').create_web_link('https://example.com', 'Example Link', 'This is the description')
print('Web Link url is {0} and its description is {1}'.format(web_link.url, web_link.description))
```

[create]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder.create_web_link
[web_link_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.web_link.WebLink

Get Web Link
------------

To get a web link object, first call [`client.web_link(web_link_id)`][web_link] to construct the appropriate 
[`WebLink`][web_link_class] object, and then calling [`web_link.get(fields=None)`][get] will return the 
[`WebLink`][web_link_class] object populated with data from the API, leaving the original object unmodified.

<!-- sample get_web_links_id -->
```python
web_link = client.web_link(web_link_id='12345').get()
print('Web Link ID is {0} and its type is {1}'.format(web_link.id, web_link.type))
```

[web_link]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.web_link
[web_link_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.web_link.WebLink
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

Update Web Link
---------------

To update a web link object, call [`web_link.update_info(data)`][update_info] with a `dict` of 
properties to update on the web link. This method returns a newly updated ['WebLink'][web_link_class] object, leaving 
the original object unmodified.

<!-- sample put_web_links_id -->
```python
updated_web_link = client.web_link(web_link_id='12345').update_info({'url': 'https://newurl.com'})
```

[update_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.update_info
[web_link_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.web_link.WebLink

Delete Web Link
---------------

To delete a web link, call [`web_link.delete()`][delete]. This method returns `True` to indicate that the deletion was 
successful.

<!-- sample delete_web_links_id -->
```python
client.web_link('12345').delete()
print('The web link was deleted!')
```

[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.delete
