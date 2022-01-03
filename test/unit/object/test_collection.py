# coding: utf-8

def test_get(mock_collection, mock_box_session):
    expected_url = mock_collection.get_url()
    collection_name = 'Favorites'

    mock_box_session.get.return_value.json.return_value = {
        'type': 'collection',
        'id': mock_collection.object_id,
        'name': collection_name,
        'collection_type': 'favorites'
    }

    fetched_collection = mock_collection.get()

    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert fetched_collection.name == collection_name


def test_get_items(mock_collection, mock_box_session):
    expected_url = mock_collection.get_url('items')
    item_id1 = '12345'
    item_id2 = '56789'

    mock_box_session.get.return_value.json.return_value = {
        'limit': 100,
        'offset': 0,
        'total_count': 2,
        'entries': [
            {
                'type': 'folder',
                'id': item_id1
            },
            {
                'type': 'file',
                'id': item_id2
            }
        ]
    }

    items = mock_collection.get_items()

    item1 = items.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={'offset': 0})
    assert item1.type == 'folder'
    assert item1.object_id == item_id1

    item2 = items.next()
    assert item2.type == 'file'
    assert item2.object_id == item_id2
