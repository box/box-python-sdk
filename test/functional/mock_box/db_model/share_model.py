# coding: utf-8

from __future__ import unicode_literals
import sqlalchemy
import uuid
from test.functional.mock_box.db_model import DbModel


class ShareModel(DbModel):
    """DB Model for Box shared links."""
    __tablename__ = 'box_share'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # pylint:disable=invalid-name
    share_id = sqlalchemy.Column(sqlalchemy.String(32), default=lambda: uuid.uuid4().hex)
    url = sqlalchemy.Column(sqlalchemy.String(50))


class ShareFileModel(ShareModel):
    """DB Model for Box shared links to files."""
    file_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('box_file.id'))


class ShareFolderModel(ShareModel):
    """DB Model for Box shared links to folders."""
    folder_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('box_folder.id'))
