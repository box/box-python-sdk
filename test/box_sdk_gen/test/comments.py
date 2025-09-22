import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.schemas.files import Files

from box_sdk_gen.managers.uploads import UploadFileAttributes

from box_sdk_gen.managers.uploads import UploadFileAttributesParentField

from box_sdk_gen.schemas.comments import Comments

from box_sdk_gen.schemas.comment_full import CommentFull

from box_sdk_gen.managers.comments import CreateCommentItem

from box_sdk_gen.managers.comments import CreateCommentItemTypeField

from box_sdk_gen.internal.utils import generate_byte_stream

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def testComments():
    file_size: int = 256
    file_name: str = get_uuid()
    file_byte_stream: ByteStream = generate_byte_stream(file_size)
    parent_id: str = '0'
    uploaded_files: Files = client.uploads.upload_file(
        UploadFileAttributes(
            name=file_name, parent=UploadFileAttributesParentField(id=parent_id)
        ),
        file_byte_stream,
    )
    file_id: str = uploaded_files.entries[0].id
    comments: Comments = client.comments.get_file_comments(file_id)
    assert comments.total_count == 0
    message: str = 'Hello there!'
    new_comment: CommentFull = client.comments.create_comment(
        message, CreateCommentItem(id=file_id, type=CreateCommentItemTypeField.FILE)
    )
    assert new_comment.message == message
    assert new_comment.is_reply_comment == False
    assert new_comment.item.id == file_id
    new_reply_comment: CommentFull = client.comments.create_comment(
        message,
        CreateCommentItem(id=new_comment.id, type=CreateCommentItemTypeField.COMMENT),
    )
    assert new_reply_comment.message == message
    assert new_reply_comment.is_reply_comment == True
    new_message: str = 'Hi!'
    client.comments.update_comment_by_id(new_reply_comment.id, message=new_message)
    new_comments: Comments = client.comments.get_file_comments(file_id)
    assert new_comments.total_count == 2
    assert new_comments.entries[1].message == new_message
    received_comment: CommentFull = client.comments.get_comment_by_id(new_comment.id)
    assert received_comment.message == new_comment.message
    client.comments.delete_comment_by_id(new_comment.id)
    with pytest.raises(Exception):
        client.comments.get_comment_by_id(new_comment.id)
    client.files.delete_file_by_id(file_id)
