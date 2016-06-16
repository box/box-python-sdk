# coding: utf-8

from __future__ import unicode_literals

from boxsdk.object.event import Event


def test_init_event(mock_box_session):
    event = Event(
        mock_box_session,
        "f82c3ba03e41f7e8a7608363cc6c0390183c3f83",
        {
            "type": "event",
            "event_id": "f82c3ba03e41f7e8a7608363cc6c0390183c3f83",
            "source":
            {
                "type": "folder",
                "id": "11446498",
            },
        },)
    assert event['type'] == 'event'
