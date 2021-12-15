# coding: utf-8

from bottle import request
from sqlalchemy.orm.exc import NoResultFound
from test.functional.mock_box.db_model.file_model import FileModel
from test.functional.mock_box.db_model.folder_model import FolderModel
from test.functional.mock_box.db_model.token_model import TokenModel
from test.functional.mock_box.util.http_utils import abort


def get_file_by_id(db_session, file_id):
    try:
        return db_session.query(FileModel).filter_by(file_id=file_id).one()
    except NoResultFound:
        abort(404)


def get_folder_by_id(db_session, folder_id):
    try:
        return db_session.query(FolderModel).filter_by(folder_id=folder_id).one()
    except NoResultFound:
        abort(404)


def get_token_record_by_token(db_session, token):
    try:
        return db_session.query(TokenModel).filter_by(token=token).one()
    except NoResultFound:
        abort(401)


def get_user_from_header(db_session):
    token = request.headers.get('Authorization')[7:]
    token_record = get_token_record_by_token(db_session, token)
    user_id = token_record.owned_by
    return user_id
