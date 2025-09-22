from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.items import Items

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import upload_new_file

client: BoxClient = get_default_client()


def testListTrashedItems():
    file: FileFull = upload_new_file()
    client.files.delete_file_by_id(file.id)
    trashed_items: Items = client.trashed_items.get_trashed_items()
    assert len(trashed_items.entries) > 0
