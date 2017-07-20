# coding: utf-8

from __future__ import unicode_literals

from boxsdk.object.recent_item import RecentItem


def test_init_recent_item(mock_box_session, mock_object_id):
    recent_item = RecentItem(
        session=mock_box_session,
        response_object={
            "type": "recent_item",
            "item": {"type": "file", "id": mock_object_id}
        })
    assert recent_item['type'] == 'recent_item'
    assert recent_item.item.object_id == mock_object_id
    assert recent_item.item.session is mock_box_session
