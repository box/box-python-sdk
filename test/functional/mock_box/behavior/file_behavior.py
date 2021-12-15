# coding: utf-8

from hashlib import sha1

from bottle import response, request
from sqlalchemy.orm import make_transient

from test.functional.mock_box.behavior.item_behavior import ItemBehavior
from test.functional.mock_box.db_model.event_model import EventModel
from test.functional.mock_box.db_model.file_model import FileModel
from test.functional.mock_box.util.db_utils import get_file_by_id, get_folder_by_id, get_user_from_header
from test.functional.mock_box.util.http_utils import abort
from test.functional.mock_box.util import json_utils as json


class FileBehavior(ItemBehavior):
    @staticmethod
    def _check_file_lock(file_object, is_download=False):
        if len(file_object.locks):
            lock_object = file_object.locks[0]
            if not is_download or lock_object.is_download_prevented:
                abort(403, 'File is locked.')

    def update_file(self, file_id):
        """
        https://developers.box.com/docs/#files-upload-a-new-version-of-a-file
        """
        file_object = get_file_by_id(self._db_session, file_id)
        self._check_file_lock(file_object)
        content = request.files.file.file.read()
        file_hash = sha1()
        file_hash.update(content)
        file_object.content = content
        file_object.sha1 = file_hash.hexdigest()
        file_object.size = len(content)
        self._db_session.add(EventModel(event_type='ITEM_UPLOAD', source_id=file_object.file_id, source_type='file'))
        self._db_session.commit()
        return json.dumps({'entries': [file_object]})

    def upload_file(self):
        """
        https://developers.box.com/docs/#files-upload-a-file
        """
        attributes = request.forms.get('attributes') or request.forms.get('metadata')
        if not attributes:
            abort(400, 'Missing parameter: attributes')
        attributes = json.loads(attributes)
        parent = attributes.get('parent')
        if parent is None or 'id' not in parent:
            abort(400, 'Missing parameter: parent(id)')
        parent_id = parent['id']
        folder = get_folder_by_id(self._db_session, parent_id)
        content = request.files.file.file.read()
        file_hash = sha1()
        file_hash.update(content)
        owner = get_user_from_header(self._db_session)
        file_object = FileModel(
            content=content,
            name=attributes.get('name', request.files.file.name),
            parent_id=folder.id,
            sha1=file_hash.hexdigest(),
            size=len(content),
            owned_by=owner,
            created_by=owner,
        )
        self._db_session.add(file_object)
        self._db_session.commit()
        self._db_session.add(EventModel(event_type='ITEM_UPLOAD', source_id=file_object.file_id, source_type='file'))
        self._db_session.commit()
        return json.dumps({'entries': [file_object]})

    def get_file_info(self, file_id):
        """
        https://developers.box.com/docs/#files-get
        """
        file_object = get_file_by_id(self._db_session, file_id)
        return json.dumps(file_object)

    def update_file_info(self, file_id):
        file_object = get_file_by_id(self._db_session, file_id)
        self._check_file_lock(file_object)
        params = json.load(request.body)
        for key, value in params.items():
            if not hasattr(FileModel, key):
                abort(400, 'File has no attribute {0}.'.format(key))
            if key == 'parent':
                # Move
                parent_id = value['id']
                parent_folder = get_folder_by_id(self._db_session, parent_id)
                file_object.parent_id = parent_folder.id
                self._db_session.add(
                    EventModel(event_type='ITEM_MOVE', source_id=file_object.file_id, source_type='file'),
                )
            else:
                setattr(file_object, key, value)
                if key == 'name':
                    self._db_session.add(
                        EventModel(event_type='ITEM_RENAME', source_id=file_object.file_id, source_type='file'),
                    )
                elif key == 'sync_state':
                    event_type = 'ITEM_SYNC' if value == 'synced' else 'ITEM_UNSYNC'
                    self._db_session.add(
                        EventModel(event_type=event_type, source_id=file_object.file_id, source_type='file'),
                    )
        self._db_session.commit()
        return json.dumps(file_object)

    def copy_file(self, file_id):
        file_object = get_file_by_id(self._db_session, file_id)
        self._check_file_lock(file_object)
        parent_folder = self._get_parent()
        self._db_session.expunge(file_object)
        make_transient(file_object)
        file_object.id = None
        file_object.file_id = None
        file_object.parent_id = parent_folder.id
        self._db_session.add(file_object)
        self._db_session.commit()
        self._db_session.add(EventModel(event_type='ITEM_COPY', source_id=file_object.file_id, source_type='file'))
        self._db_session.commit()
        return json.dumps(file_object)

    def download_file(self, file_id):
        """
        https://developers.box.com/docs/#files-download-a-file
        """
        file_object = get_file_by_id(self._db_session, file_id)
        self._check_file_lock(file_object, is_download=True)
        return file_object.content

    def delete_file(self, file_id):
        file_object = get_file_by_id(self._db_session, file_id)
        self._check_file_lock(file_object)
        self._db_session.delete(file_object)
        self._db_session.add(EventModel(event_type='ITEM_TRASH', source_id=file_object.file_id, source_type='file'))
        self._db_session.commit()
        response.status = 204
