# coding: utf-8

from bottle import request, response
from sqlalchemy.orm import make_transient
from sqlalchemy.orm.exc import NoResultFound

from boxsdk.object.folder import FolderSyncState
from test.functional.mock_box.behavior.item_behavior import ItemBehavior
from test.functional.mock_box.db_model.event_model import EventModel
from test.functional.mock_box.db_model.file_model import FileModel
from test.functional.mock_box.db_model.folder_model import FolderModel
from test.functional.mock_box.util.db_utils import get_folder_by_id, get_user_from_header
from test.functional.mock_box.util.http_utils import abort
from test.functional.mock_box.util import json_utils as json


class FolderBehavior(ItemBehavior):
    def get_folder_info(self, folder_id):
        """
        https://developers.box.com/docs/#folders-get-information-about-a-folder
        """
        folder = get_folder_by_id(self._db_session, folder_id)
        return json.dumps(folder)

    def update_folder_info(self, folder_id):
        folder = get_folder_by_id(self._db_session, folder_id)
        params = json.load(request.body)
        for key, value in params.items():
            if not hasattr(FolderModel, key):
                abort(400, 'Folder has no attribute {0}.'.format(key))
            if key == 'parent':
                # Move
                parent_id = value['id']
                parent_folder = get_folder_by_id(self._db_session, parent_id)
                folder.parent_id = parent_folder.id
                self._db_session.add(
                    EventModel(event_type='ITEM_MOVE', source_id=folder.folder_id, source_type='folder'),
                )
            else:
                setattr(folder, key, value)
                if key == 'name':
                    self._db_session.add(
                        EventModel(event_type='ITEM_RENAME', source_id=folder.folder_id, source_type='folder'),
                    )
                elif key == 'sync_state':
                    event_type = 'ITEM_SYNC' if value == FolderSyncState.IS_SYNCED else 'ITEM_UNSYNC'
                    self._db_session.add(
                        EventModel(event_type=event_type, source_id=folder.folder_id, source_type='folder'),
                    )
        self._db_session.commit()
        return json.dumps(folder)

    def copy_folder(self, folder_id):
        folder = get_folder_by_id(self._db_session, folder_id)
        parent_folder = self._get_parent()
        self._db_session.expunge(folder)
        make_transient(folder)
        folder.id = None
        folder.folder_id = None
        folder.parent_id = parent_folder.id
        self._db_session.add(folder)
        self._db_session.commit()
        self._db_session.add(EventModel(event_type='ITEM_COPY', source_id=folder.folder_id, source_type='folder'))
        self._db_session.commit()
        return json.dumps(folder)

    def delete_folder(self, folder_id):
        folder = get_folder_by_id(self._db_session, folder_id)
        self._db_session.delete(folder)
        self._db_session.commit()
        self._db_session.add(EventModel(event_type='ITEM_TRASH', source_id=folder.folder_id, source_type='folder'))
        response.status = 204

    def _gat(self, folder_id):
        # pylint:disable=unused-argument
        files = self._db_session.query(FileModel).all()
        folders = self._db_session.query(FolderModel).filter(FolderModel.folder_id != '0').all()
        return json.dumps({'items': files + folders})

    def get_folder_items(self, folder_id):
        view = request.params.get('view', None)
        if view is not None and view == 'subfolder_sync_forked_tree':
            return self._gat(folder_id)
        limit = int(request.params.get('limit', 100))
        offset = int(request.params.get('offset', 0))
        # fields = request.params.get('fields')
        # fields = set(fields.split(',')) if fields else set() | set(['name'])
        folder = get_folder_by_id(self._db_session, folder_id)
        folder_count = self._db_session.query(FolderModel).filter_by(parent_id=folder.id).count()
        folders = []
        if folder_count > offset:
            folders = self._db_session.query(
                FolderModel,
            ).filter_by(parent_id=folder.id).limit(limit).offset(offset).all()
        files = []
        if len(folders) < limit:
            limit -= len(folders)
            offset -= folder_count
            files = self._db_session.query(FileModel).filter_by(parent_id=folder.id).limit(limit).offset(offset).all()
        items = folders + files
        return json.dumps({'total_count': len(items), 'entries': items})

    def create_folder(self):
        """
        https://developers.box.com/docs/#folders-create-a-new-folder
        """
        params = json.load(request.body)
        name = params.get('name')
        if name is None:
            abort(400, 'Missing parameter: name')
        parent = params.get('parent')
        if parent is None or 'id' not in parent:
            abort(400, 'Missing parameter: parent(id)')
        parent_id = parent['id']
        try:
            parent_folder = self._db_session.query(FolderModel).filter_by(folder_id=parent_id).one()
        except NoResultFound:
            abort(404)
        owner = get_user_from_header(self._db_session)
        name_in_use = self._db_session.query(FolderModel).filter_by(name=name).count()
        if name_in_use:
            abort(409, 'An item with that name already exists.')
        folder = FolderModel(name=name, parent_id=parent_folder.id, owned_by=owner, created_by=owner)
        self._db_session.add(folder)
        self._db_session.commit()
        self._db_session.add(EventModel(event_type='ITEM_CREATE', source_id=folder.folder_id, source_type='folder'))
        self._db_session.commit()
        return json.dumps(folder)
