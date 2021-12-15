# coding: utf-8

import uuid
import sqlalchemy
from sqlalchemy.orm import relationship
from test.functional.mock_box.db_model import DbModel


_user_group_table = sqlalchemy.Table(
    'user_group_association',
    DbModel.metadata,
    sqlalchemy.Column('group_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('box_group.id')),
    sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('box_user.id'))
)


class GroupModel(DbModel):
    """DB Model for Box groups."""
    __tablename__ = 'box_group'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # pylint:disable=invalid-name
    group_id = sqlalchemy.Column(sqlalchemy.String(32), default=lambda: uuid.uuid4().hex)
    name = sqlalchemy.Column(sqlalchemy.String(255))
    users = relationship('UserModel', secondary=_user_group_table, backref='groups')
