# coding: utf-8

from __future__ import unicode_literals
from datetime import datetime
import uuid
import sqlalchemy
from sqlalchemy.orm import backref, relationship
from test.functional.mock_box.db_model import DbModel


class FolderModel(DbModel):
    """DB Model for Box folders."""
    __tablename__ = 'box_folder'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # pylint:disable=invalid-name
    folder_id = sqlalchemy.Column(sqlalchemy.String(32), default=lambda: uuid.uuid4().hex)
    name = sqlalchemy.Column(sqlalchemy.String(255))
    files = relationship('FileModel', backref='parent', cascade='save-update, delete')
    parent_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('box_folder.id'))
    folders = relationship('FolderModel', backref=backref('parent', remote_side=[id]), cascade='save-update, delete')
    created_by_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('box_user.id'))
    created_by = relationship('UserModel', foreign_keys=[created_by_id])
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    modified_at = sqlalchemy.Column(sqlalchemy.DateTime, onupdate=datetime.now)
    owned_by_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('box_user.id'))
    collaborations = relationship('CollaborationModel', backref='item', cascade='save-update, delete')
    shared_link = relationship(
        'ShareFolderModel',
        backref=backref('shared_folder', remote_side=[id]),
        cascade='save-update, delete',
    )
    sync_state = sqlalchemy.Column(sqlalchemy.Enum('not_synced', 'partially_synced', 'synced'), default='not_synced')
    sequence_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    etag = sqlalchemy.Column(sqlalchemy.String(32), default=lambda: uuid.uuid4().hex)

    __mapper_args__ = {
        "version_id_col": sequence_id,
    }
