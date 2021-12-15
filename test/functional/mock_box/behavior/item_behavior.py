# coding: utf-8

from bottle import request
from test.functional.mock_box.util.db_utils import get_folder_by_id
from test.functional.mock_box.util.http_utils import abort
from test.functional.mock_box.util import json_utils as json


class ItemBehavior:
    def __init__(self, db_session):
        self._db_session = db_session

    def _get_parent(self):
        params = json.load(request.body)
        parent = params.get('parent')
        if parent is None or 'id' not in parent:
            abort(400, 'Missing parameter: parent(id)')
        parent_id = parent['id']
        return get_folder_by_id(self._db_session, parent_id)
