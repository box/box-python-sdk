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
- [Move a Web Link](#move-a-web-link)
- [Copy a Web Link](#copy-a-web-link)
- [Rename a Web Link](#rename-a-web-link)
- [Delete Web Link](#delete-web-link)
- [Create a Shared Link](#create-a-shared-link)
- [Update a Shared Link](#update-a-shared-link)
- [Get a Shared Link](#get-a-shared-link)
- [Remove a Shared Link](#remove-a-shared-link)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Create Web Link
---------------

To create a web link object, calling [`folder.create_web_link(target_url, name=None, description=None)`][create] 
will let you create a new web link with a specified name and description. This method return an newly created [`WebLink`][web_link_class] 
object populated with data from the API, leaving the original object unmodified.

<!-- sample post_web_links -->
```python
web_link = client.folder(folder_id='12345').create_web_link('https://example.com', 'Example Link', 'This is the description')
print(f'Web Link url is {web_link.url} and its description is {web_link.description}')
```

[create]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.folder.Folder.create_web_link
[web_link_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.web_link.WebLink

Get Web Link
------------

To get a web link object, first call [`client.web_link(web_link_id)`][web_link] to construct the appropriate 
[`WebLink`][web_link_class] object, and then calling [`web_link.get(*, fields=None, headers=None, **kwargs)`][get]
will return the [`WebLink`][web_link_class] object populated with data from the API, leaving the original object unmodified.

<!-- sample get_web_links_id -->
```python
web_link = client.web_link(web_link_id='12345').get()
print(f'Web Link ID is {web_link.id} and its type is {web_link.type}')
```

[web_link]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.web_link
[web_link_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.web_link.WebLink
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get

Update Web Link
---------------

To update a web link object, call [`web_link.update_info(data=data_to_update)`][update_info] with a `dict` of 
properties to update on the web link. This method returns a newly updated ['WebLink'][web_link_class] object, leaving 
the original object unmodified.

```python
updated_web_link = client.web_link(web_link_id='12345').update_info(data={'url': 'https://newurl.com'})
```

[update_info]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.update_info
[web_link_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.web_link.WebLink

Move a Web Link
-----------

To move a web link from one folder into another, call [`web_link.move(parent_folder, name=None)`][move] with the destination
folder to move the web link into.  You can optionally provide a `name` parameter to automatically rename the web link
in case of a name conflict in the destination folder. This method returns the updated [`WebLink`][web_link_class]
object in the new folder.

```python
web_link_id = '11111'
destination_folder_id = '44444'

web_link_to_move = client.web_link(web_link_id)
destination_folder = client.folder(destination_folder_id)

moved_web_link = web_link_to_move.move(destination_folder)
print(f'Web link "{moved_web_link.name}" has been moved into folder "{moved_web_link.parent.name}"')
```

[move]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_item.BaseItem.move

Copy a Web Link
-----------

A web link can be copied to a new folder by calling [`web_link.copy(*, parent_folder, name=None, **_kwargs)`][copy] 
with the destination folder and an optional new name for the web link in case there is a name conflict in the
destination folder. This method returns a [`WebLink`][web_link_class] object representing the copy of the web link 
in the destination folder.

<!-- sample post_web_links_id_copy -->
```python
web_link = client.web_link(web_link_id='12345')

web_link_copy = web_link_to_copy.copy(parent_folder=destination_folder)
print(f'Web link "{web_link_copy.name}" has been copied into folder "{web_link_copy.parent.name}"')
```

[copy]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_item.BaseItem.copy

Rename a Web Link
-----------

A web link can be renamed by calling [`web_link.rename(name)`][rename]. This method returns the updated
[`WebLink`][web_link_class] object with a new name.

```python
web_link = client.web_link(web_link_id='12345')

renamed_web_link = web_link.rename("new-name")
print(f'Web link was renamed to "{renamed_web_link.name}"')
```

[rename]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_item.BaseItem.rename


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

Create a Shared Link
--------------------

A shared link for a web link can be generated by calling
[`web_link.get_shared_link(*, access=None, unshared_at=SDK_VALUE_NOT_SET, password=None,
vanity_name=None, **kwargs)`][get_shared_link]. This method returns a `unicode` string containing the shared link URL.

<!-- sample put_web_links_id add_shared_link -->
```python
url = client.web_link('12345').get_shared_link(access='open')
print(f'The web link shared link URL is: {url}')
```

[get_shared_link]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.web_link.WebLink.get_shared_link

Update a Shared Link
--------------------

A shared link for a web link can be updated by calling
[`web_link.get_shared_link(*, access=None, unshared_at=SDK_VALUE_NOT_SET, password=None,
vanity_name=None, **kwargs)`][update_shared_link] with an updated list of properties.

This method returns a `unicode` string containing the shared link URL.

<!-- sample put_web_links_id update_shared_link -->
```python
url = client.web_link('12345').get_shared_link(access='open', password='letmein')
print(f'The web link shared link URL is: {url}')
```

[update_shared_link]:
https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.web_link.WebLink.get_shared_link

Get a Shared Link
--------------------

To check for an existing shared link on a web link, simply call `web_link.shared_link`
This method returns a `unicode` string containing the shared link URL.

<!-- sample get_web_links_id get_shared_link -->
```python
shared_link = client.web_link('12345').get().shared_link
url = shared_link['url']
```

Remove a Shared Link
--------------------

A shared link for a web link can be removed by calling [`web_link.remove_shared_link(**kwargs)`][remove_shared_link].

<!-- sample put_web_links_id remove_shared_link -->
```python
client.web_link('12345').remove_shared_link()
```

[remove_shared_link]:
https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.web_link.WebLink.remove_shared_link
