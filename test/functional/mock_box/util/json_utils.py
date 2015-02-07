# coding: utf-8

from __future__ import unicode_literals
import codecs
import json
from test.functional.mock_box.db_model.file_model import FileModel
from test.functional.mock_box.db_model import DbModel


def serializer_factory(cls):

    class BoxObjectSerializer(json.JSONEncoder):
        # pylint:disable=method-hidden
        _blacklist = ['metadata', 'files', 'folders']
        _cls = cls

        def default(self, o):
            if hasattr(o, 'isoformat'):
                return o.isoformat()
            if isinstance(o, DbModel):
                if DbModel not in self._cls.__bases__:
                    self._cls = o.__class__
                fields = {}
                for field in (x for x in dir(o) if not x.startswith('_') and x not in self._blacklist):
                    data = o.__getattribute__(field)
                    if isinstance(o, self._cls):
                        fields[field] = data
                    else:
                        try:
                            json.dumps(data)
                            fields[field] = data
                        except (TypeError, UnicodeDecodeError):
                            fields[field] = None
                object_type = type(o).__name__.lower()[:-5]
                fields['type'] = object_type
                object_id = object_type + '_id'
                if hasattr(o, 'id') and hasattr(o, object_id):
                    fields['id'] = o.__getattribute__(object_id)
                    del fields[object_id]
                if isinstance(o, FileModel):
                    del fields['content']
                return fields
            return super(BoxObjectSerializer, self).default(o)

    return BoxObjectSerializer


def loads(string, **kwargs):
    return json.loads(string, **kwargs)


def load(file_pointer, **kwargs):
    reader = codecs.getreader('utf-8')
    return json.load(reader(file_pointer), **kwargs)


def dump(obj, file_pointer, **kwargs):
    return json.dump(obj, file_pointer, cls=serializer_factory(obj.__class__), check_circular=False, **kwargs)


def dumps(obj, **kwargs):
    return json.dumps(obj, cls=serializer_factory(obj.__class__), check_circular=False, **kwargs)
