Comments
========

Comment objects represent a user-created comment on a file. They can be added directly to a file.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Get Information About a Comment](#get-information-about-a-comment)
- [Get the Comments on a File](#get-the-comments-on-a-file)
- [Add a Comment to a File](#add-a-comment-to-a-file)
- [Reply to a Comment](#reply-to-a-comment)
- [Edit a Comment](#edit-a-comment)
- [Delete a Comment](#delete-a-comment)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Get Information About a Comment
-------------------------------

To get a specific comment object, first call `[client.comment(comment_id)`][comment] to construct the appropriate
[`Comment`][comment_class] object, and then call [`comment.get(*, fields=None, headers=None, **kwargs)`][get] to
retrieve the data about the comment. The latter method returns a new [`Comment`][comment_class] object with fields
populated by data from the API, leaving the original unmodified.

<!-- sample get_comment_id -->
```python
comment = client.comment(comment_id='55555').get()
print(f'The comment says "{comment.message}"')
```

[comment]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.client.html#boxsdk.client.client.Client.comment
[get]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.get
[comment_class]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.comment.Comment

Get the Comments on a File
--------------------------

To retrieve the comment left on a file, call [`file.get_comments(limit=None, offset=0, fields=None)`][get_comments].
This method returns a `BoxObjectCollection` that you can use to iterate over all the
[`Comment`][comment_class] objects in the set.

<!-- sample get_files_id_comments -->
```python
comments = client.file(file_id='11111').get_comments()
for comment in comments:
    print(f'Comment was left by {comment.created_by.name} at {comment.created_at}')
```

[get_comments]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.get_comments

Add a Comment to a File
-----------------------

To leave a comment on a file, call [`file.add_comment(message)`][add_comment] with the message to leave in the comment.

<!-- sample post_comments -->
```python
comment = client.file(file_id='11111').add_comment('When should I have this done by?')
```

You can at-mention other users by adding special tags within the message, in the format `@[USER_ID:USER_NAME]`.  For
example, to at-mention John Doe, whose user ID is `"33333"`: `@[33333:John Doe]`.

<!-- sample post_comments tag_user  -->
```python
comment = client.file(file_id='11111').add_comment('Hey @[44444:boss], when should I have this done by?')
```

This method returns a [`Comment`][comment_class] object representing the newly-created comment.

[add_comment]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.file.File.add_comment

Reply to a Comment
------------------

To reply to a comment, call [`comment.reply(message)`][reply] with the message to leave in the comment.

<!-- sample post_comments as_reply  -->
```python
reply_comment = client.comment(comment_id='12345').reply('If possible, please finish this by the end of the week!')
```

You can at-mention other users by adding special tags within the message, in the format `@[USER_ID:USER_NAME]`.  For
example, to at-mention John Doe, whose user ID is `"33333"`: `@[33333:John Doe]`.

<!-- sample post_comments as_reply_tag_user  -->
```python
reply_comment = client.comment(comment_id='12345').reply('@[33333:John Doe], if possible, please finish this by the end of the week!')
```

This method returns a [`Comment`][comment_class] object representing the newly-created comment.

[reply]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.comment.Comment.reply

Edit a Comment
--------------

To edit a comment and change its message, call [`comment.edit(message)`][edit] with the message to leave in the comment.
You can at-mention other users by adding special tags within the message, in the format `@[USER_ID:USER_NAME]`.  For
example, to at-mention John Doe, whose user ID is `"33333"`: `@[33333:John Doe]`.  This method returns an updated
[`Comment`][comment_class] object, leaving the original unmodified.

<!-- sample put_comments_id -->
```python
edited_comment = client.comment(comment_id='98765').edit('If possible, please finish this by Friday!')
```

[edit]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.comment.Comment.edit

Delete a Comment
----------------

To delete a comment, call [`comment.delete()`][delete].  This will remove the comment from the file.  This method
returns `True` to indicate that the deletion succeeded.

<!-- sample delete_comments_id -->
```python
client.comment(comment_id='12345').delete()
```

[delete]: https://box-python-sdk.readthedocs.io/en/latest/boxsdk.object.html#boxsdk.object.base_object.BaseObject.delete
