# coding: utf-8

from __future__ import unicode_literals
import json
import pytest

from boxsdk.object.comment import Comment

# pylint:disable=protected-access
# pylint:disable=redefined-outer-name

@pytest.mark.parametrize(
    'message_type, message',
    [
        # Test case for plain message
        (
            'message',
            'Hello there!'
        ),

        # Test case for tagged message
        (
            'tagged_message',
            '@[22222:Test User] Hi!'
        )
    ]
)
def test_reply(test_comment, mock_box_session, message_type, message):
    expected_url = mock_box_session.get_url('comments')
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
    assert reply_comment.object_id == '12345'

@pytest.mark.parametrize(
    'message_type, message',
    [
        # Test case for plain message
        (
            'message',
            'Hello there!'
        ),

        # Test case for tagged message
        (
            'tagged_message',
            '@[22222:Test User] Hi!'
        )
    ]
)
def test_edit(test_comment, mock_box_session, message_type, message):
    expected_url = mock_box_session.get_url('comments', test_comment.object_id)
    expected_data = {
        message_type: message,
    }
    mock_box_session.post.return_value.json.return_value = {
        'type': 'comment',
        'id': '12345',
        message_type: message
    }
    test_comment.edit(message)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(expected_data), headers=None, params=None)

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
    assert comment.message == 'Hi!' # pylint:disable=no-member

def test_delete(test_comment, mock_box_session):
    expected_url = test_comment.get_url()
    test_comment.delete()
    mock_box_session.delete.assert_called_once_with(expected_url, expect_json_response=False, headers=None, params={})
