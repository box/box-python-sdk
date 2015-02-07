# coding: utf-8

from __future__ import unicode_literals
from sqlalchemy.orm.exc import NoResultFound
from test.functional.mock_box.db_model.user_model import UserModel
from test.functional.mock_box.util.db_utils import get_user_from_header
from test.functional.mock_box.util.http_utils import abort


class UserBehavior(object):
    def __init__(self, db_session):
        self._db_session = db_session

    def _get_user_by_id(self, user_id):
        try:
            return self._db_session.query(UserModel).filter_by(user_id=user_id).one()
        except NoResultFound:
            abort(401)

    def get_user_info(self, user_id):
        if user_id == 'me':
            user_id = get_user_from_header(self._db_session).user_id
        else:
            user_id = int(user_id)
        user = self._get_user_by_id(user_id)
        return {
            'type': 'user',
            'login': user.login,
            'enterprise': None,
            'id': user.user_id,
            'name': user.name,
        }
