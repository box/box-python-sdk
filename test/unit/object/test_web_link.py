# coding: utf-8

from __future__ import unicode_literals


def test_get(mock_box_session, test_web_link):
    # pylint:disable=redefined-outer-name, protected-access
    web_link_id = test_web_link.object_id
    expected_url = mock_box_session.get_url('web_links', web_link_id)

    mock_web_link = {
        'type': 'web_link',
        'url': 'https://test/com',
        'id': 1234,
        'created_at': '2015-05-07T15:00:01-07:00',
    }

    mock_box_session.get.return_value.json.return_value = mock_web_link
    web_link = test_web_link.get()

    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert web_link.id == mock_web_link['id']
    assert web_link.type == mock_web_link['type']
    assert web_link.url == mock_web_link['url']



def test_delete(mock_box_session, test_web_link):
    web_link_id = test_web_link.object_id
    expected_url = mock_box_session.get_url('web_links', web_link_id)
    test_web_link.delete()
    mock_box_session.delete.assert_called_once_with(expected_url, expect_json_response=False, headers=None, params={})

