# coding: utf-8

from datetime import datetime
import sqlalchemy
from sqlalchemy.orm import relationship, backref
import uuid
from test.functional.mock_box.db_model import DbModel


class FileModel(DbModel):
    """DB Model for Box files."""
    __tablename__ = 'box_file'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # pylint:disable=invalid-name
    file_id = sqlalchemy.Column(sqlalchemy.String(32), default=lambda: str(uuid.uuid4().int))
    name = sqlalchemy.Column(sqlalchemy.String(255))
    parent_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('box_folder.id'))
    content = sqlalchemy.Column(sqlalchemy.LargeBinary)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    modified_at = sqlalchemy.Column(sqlalchemy.DateTime, onupdate=datetime.now)
    created_by_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('box_user.id'))
    created_by = relationship('UserModel', foreign_keys=[created_by_id])
    owned_by_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('box_user.id'))
    shared_link = relationship(
        'ShareFileModel',
        backref=backref('shared_file', remote_side=[id]),
        cascade='save-update, delete',
    )
    locks = relationship('LockModel', backref='item', cascade='save-update, delete')
    etag = sqlalchemy.Column(sqlalchemy.String(32), default=lambda: uuid.uuid4().hex)
    sequence_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    sha1 = sqlalchemy.Column(sqlalchemy.String(40))
    size = sqlalchemy.Column(sqlalchemy.Integer)

    __mapper_args__ = {
        "version_id_col": sequence_id,
    }
