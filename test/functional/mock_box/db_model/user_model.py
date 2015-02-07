# coding: utf-8

from __future__ import unicode_literals
import sqlalchemy
import uuid
from sqlalchemy.orm import relationship
from test.functional.mock_box.db_model import DbModel


class UserModel(DbModel):
    """DB Model for Box users."""
    __tablename__ = 'box_user'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # pylint:disable=invalid-name
    user_id = sqlalchemy.Column(sqlalchemy.String(32), default=lambda: uuid.uuid4().hex)
    name = sqlalchemy.Column(sqlalchemy.String(255))
    login = sqlalchemy.Column(sqlalchemy.String(255))
    owned_files = relationship(
        'FileModel',
        backref='owned_by',
        cascade='save-update, delete',
        foreign_keys='[FileModel.owned_by_id]',
    )
    owned_folders = relationship(
        'FolderModel',
        backref='owned_by',
        cascade='save-update, delete',
        foreign_keys='[FolderModel.owned_by_id]',
    )
    created_collaborations = relationship('CollaborationModel', backref='created_by', cascade='save-update, delete')
    created_locks = relationship('LockModel', backref='created_by', cascade='save-update, delete')
    authorized_application_tokens = relationship('TokenModel', backref='owned_by', cascade='save-update, delete')
