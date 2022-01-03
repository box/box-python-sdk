# coding: utf-8

import json

from boxsdk.object.comment import Comment


# pylint:disable=protected-access
# pylint:disable=redefined-outer-name

def test_reply(test_comment, mock_box_session, comment_params):
    expected_url = mock_box_session.get_url('comments')
    message_type, message = comment_params
    expected_data = {
        message_type: message,
        'item': {
            'type': 'comment',
            'id': test_comment.object_id
        }
    }
    mock_box_session.post.return_value.json.return_value = {
        'type': 'comment',
        'id': '12345',
        message_type: message
    }
    reply_comment = test_comment.reply(message)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data))
    assert isinstance(reply_comment, Comment)
    assert reply_comment.object_id == '12345'


def test_edit(test_comment, mock_box_session, comment_params):
    expected_url = mock_box_session.get_url('comments', test_comment.object_id)
    message_type, message = comment_params
    expected_data = {
        message_type: message,
    }
    mock_box_session.put.return_value.json.return_value = {
        'type': 'comment',
        'id': '12345',
        message_type: message
    }
    updated_comment = test_comment.edit(message)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(expected_data), headers=None, params=None)
    assert isinstance(updated_comment, Comment)
    assert updated_comment[message_type] == message


def test_get(mock_box_session):
    comment_id = '1235'
    expected_url = mock_box_session.get_url('comments', comment_id)
    mock_box_session.get.return_value.json.return_value = {
        'type': 'comment',
        'id': comment_id,
        'message': 'Hi!'
    }
    comment = Comment(mock_box_session, comment_id).get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert comment.object_id == comment_id
    assert comment.message == 'Hi!'  # pylint:disable=no-member


def test_delete(test_comment, mock_box_session):
    expected_url = test_comment.get_url()
    test_comment.delete()
    mock_box_session.delete.assert_called_once_with(expected_url, expect_json_response=False, headers=None, params={})
