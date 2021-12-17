# coding: utf-8

from datetime import datetime, timedelta
from threading import Event

from bottle import request
from sqlalchemy import event

from test.functional.mock_box.db_model.event_model import EventModel
from test.functional.mock_box.db_model.file_model import FileModel
from test.functional.mock_box.db_model.folder_model import FolderModel
from test.functional.mock_box.util import json_utils as json


class EventBehavior:
    def __init__(self, db_session):
        self._db_session = db_session
        self._subscribe_event = Event()
        self._epoch = datetime.utcnow()

        def handle_event(*_):
            self._subscribe_event.set()

        event.listen(EventModel, 'after_insert', handle_event)

    def _ms_since_epoch(self, when):
        delta = when - self._epoch
        total_seconds = (delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 10 ** 6) / 10 ** 6
        return int(total_seconds * 1000)

    def _ms_after_epoch(self, when):
        return self._epoch + timedelta(seconds=when / 1000)

    def get_events(self):
        stream_position = request.params.get('stream_position', '0')
        limit = int(request.params.get('limit', '100'))
        if stream_position == 'now':
            return json.dumps({
                'total_count': 0,
                'next_stream_position': self._ms_since_epoch(datetime.utcnow()),
                'entries': [],
            })
        stream_position = int(stream_position)
        event_query = self._db_session.query(EventModel).filter(
            EventModel.stream_position >= self._ms_after_epoch(stream_position or 1),
        )
        total_count = event_query.count()
        results = event_query.order_by(EventModel.sequence_id).limit(limit).all()
        max_stream_position = max(e.stream_position for e in results) if results else self._epoch
        next_stream_position = datetime.utcnow() if total_count < limit else max_stream_position - timedelta(seconds=5)
        file_ids = [e.source_id for e in results if e.source_type == 'file']
        folder_ids = [e.source_id for e in results if e.source_type == 'folder']
        file_records = self._db_session.query(FileModel).filter(FileModel.file_id.in_(file_ids)).all() if file_ids else []
        folder_records = self._db_session.query(FolderModel).filter(FolderModel.folder_id.in_(folder_ids)).all() if folder_ids else []
        if results:
            results = [{
                'type': 'event',
                'event_id': e.event_id,
                'event_type': e.event_type,
                'source_id': e.source_id,
                'source': next(
                    (f for f in file_records if f.file_id == e.source_id),
                    None
                ) or next((f for f in folder_records if f.folder_id == e.source_id), None),
            } for e in results]
        return json.dumps({
            'chunk_size': total_count,
            'next_stream_position': self._ms_since_epoch(next_stream_position),
            'entries': results,
        })

    @staticmethod
    def get_long_poll_url():
        return {
            'chunk_size': 1,
            'entries': [{
                'type': 'realtime_server',
                'url': 'http://localhost:18089/subscribe?channel=cc807c9c4869ffb1c81a&stream_type=all',
                'ttl': 10,
                'max_retries': 10,
                'retry_timeout': 610,
            }]
        }

    def subscribe(self):
        if self._subscribe_event.isSet():
            self._subscribe_event.clear()
            return {
                'message': 'new_change'
            }
        got_event = self._subscribe_event.wait(timeout=600)
        if got_event:
            self._subscribe_event.clear()
            return {
                'message': 'new_change'
            }
        else:
            return {
                'message': 'reconnect'
            }
