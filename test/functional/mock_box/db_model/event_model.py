# coding: utf-8

from __future__ import unicode_literals
from datetime import datetime
import sqlalchemy
import uuid
from test.functional.mock_box.db_model import DbModel


class EventModel(DbModel):
    """DB Model for Box events."""
    __tablename__ = 'box_event'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # pylint:disable=invalid-name
    event_id = sqlalchemy.Column(sqlalchemy.String(32), default=lambda: uuid.uuid4().hex)
    stream_position = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)
    created_by_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('box_user.id'))
    event_type = sqlalchemy.Column(sqlalchemy.Enum(
        'ITEM_CREATE',
        'ITEM_UPLOAD',
        'ITEM_MOVE',
        'ITEM_COPY',
        'LOCK_CREATE',
        'LOCK_DESTROY',
        'ITEM_TRASH',
        'ITEM_UNDELETE_VIA_TRASH',
        'COLLAB_ADD_COLLABORATOR',
        'COLLAB_REMOVE_COLLABORATOR',
        'ITEM_SYNC',
        'ITEM_UNSYNC',
        'ITEM_RENAME',
    ))
    source_id = sqlalchemy.Column(sqlalchemy.Integer)
    source_type = sqlalchemy.Column(sqlalchemy.Enum('file', 'folder'))
    sequence_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    __mapper_args__ = {
        "version_id_col": sequence_id,
    }
