# coding: utf-8

import sqlalchemy
from sqlalchemy.orm import relationship
from test.functional.mock_box.db_model import DbModel


_user_app_table = sqlalchemy.Table(
    'user_app_association',
    DbModel.metadata,
    sqlalchemy.Column('app_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('box_application.id')),
    sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('box_user.id'))
)


class ApplicationModel(DbModel):
    """DB Model for Box users."""
    __tablename__ = 'box_application'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # pylint:disable=invalid-name
    client_id = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)
    client_secret = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)
    auth_tokens = relationship('TokenModel', backref='application', cascade='save-update, delete')
    users = relationship('UserModel', secondary=_user_app_table, backref='apps')
