# coding: utf-8

import json
import pytest

from mock import ANY
from boxsdk.config import API
from boxsdk.object.file import File
from boxsdk.object.user import User
from boxsdk.object.search import MetadataSearchFilters, MetadataSearchFilter, SearchScope, TrashContent


@pytest.fixture
def search_query():
    return 'myquery'


@pytest.fixture(params=(1, 20, 100))
def search_limit(request):
    return request.param


@pytest.fixture(params=(0, 10))
def search_offset(request):
    return request.param


@pytest.fixture(params=(None, 'file', 'folder'))
def search_result_type(request):
    return request.param


@pytest.fixture(params=(None, ('name',), ('name', 'description')))
def search_content_types(request):
    return request.param


@pytest.fixture
def search_value_based_filters():
    metadata_filters = MetadataSearchFilters()
    metadata_filter = MetadataSearchFilter(template_key='mytemplate', scope='enterprise')
    metadata_filter.add_value_based_filter(field_key='myfield', value='myvalue')
    metadata_filters.add_filter(metadata_filter)
    return metadata_filters


@pytest.fixture(params=(
    {'gt_value': 'mygtvalue'},
    {'lt_value': 'myltvalue'},
    {'gt_value': 'mygtvalue', 'lt_value': 'myltvalue'}
))
def search_range_filters(request):
    metadata_filters = MetadataSearchFilters()
    metadata_filter = MetadataSearchFilter(template_key='mytemplate', scope='enterprise')
    filter_params = {'field_key': 'myfield'}
    filter_params.update(request.param)
    metadata_filter.add_range_filter(**filter_params)
    metadata_filters.add_filter(metadata_filter)
    return metadata_filters


@pytest.fixture
def search_entries():
    return [
        {'id': '1234', 'type': 'file'}
    ]


@pytest.fixture
def search_response():
    entries = search_entries()
    return {
        'entries': entries,
        'total_count': len(entries),
        'limit': 20,
        'offset': 0
    }


@pytest.fixture
def metadata_query_response():
    return {
        'entries': [
            {
                'type': 'file',
                'id': '1244738582',
                'name': 'Very Important.docx',
                'metadata': {
                    'enterprise_67890': {
                        'catalogImages': {
                            '$parent': 'file_50347290',
                            '$version': 2,
                            '$template': 'catalogImages',
                            '$scope': 'enterprise_67890',
                            'photographer': 'Bob Dylan'
                        }
                    }
                }
            },
            {
                'type': 'folder',
                'id': '124242482',
                'name': 'Also Important.docx',
                'metadata': {
                    'enterprise_67890': {
                        'catalogImages': {
                            '$parent': 'file_50427291',
                            '$version': 2,
                            '$template': 'catalogImages',
                            '$scope': 'enterprise_67890',
                            'photographer': 'Bob Dylan'
                        }
                    }
                }
            }
        ],
        'limit': 2,
        'next_marker': ''
    }


@pytest.fixture
def search_with_shared_links_entries():
    return [
        {
            'accessible_via_shared_link': 'https://www.box.com/s/vspke7y05sb214wjokpk',
            'item': {'id': '1234', 'type': 'file'},
            'type': 'search_result'
        },
        {
            'accessible_via_shared_link': None,
            'item': {'id': '1234', 'type': 'file'},
            'type': 'search_result'
        }
    ]


@pytest.fixture
def search_with_shared_links_response():
    entries = search_with_shared_links_entries()
    return {
        'entries': entries,
        'total_count': len(entries),
        'limit': 20,
        'offset': 0
    }


class Matcher:
    def __init__(self, compare, some_obj):
        self.compare = compare
        self.some_obj = some_obj

    def __eq__(self, other):
        return self.compare(self.some_obj, other)


def compare_params(self, other):
    if not isinstance(self, dict) or not isinstance(other, dict):
        return False
    for key in self:
        # We need to ensure that the JSON-encoded mdfilters matches regardless of key order
        if key == 'mdfilters':
            if json.loads(self['mdfilters']) != json.loads(other['mdfilters']):
                return False
        # For other keys, just ensure that they are equal
        elif key in ('type', 'content_types'):
            return self[key] is None or self[key] == other[key]
        else:
            if self[key] != other[key]:
                return False
    return True


def test_query_with_value_based_filters(
        mock_box_session,
        make_mock_box_request,
        test_search,
        search_query,
        search_limit,
        search_offset,
        search_value_based_filters,
        search_response,
        search_entries,
        search_result_type,
        search_content_types,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value, _ = make_mock_box_request(response=search_response)
    response = test_search.query(
        search_query,
        limit=search_limit,
        offset=search_offset,
        metadata_filters=search_value_based_filters,
        result_type=search_result_type,
        content_types=search_content_types,
    )
    for actual, expected in zip(response, [File(mock_box_session, item['id'], item) for item in search_entries]):
        assert actual == expected

    mock_box_session.get.assert_called_once_with(
        test_search.get_url(),
        params=Matcher(compare_params, {
            'query': search_query,
            'limit': search_limit,
            'mdfilters': json.dumps(search_value_based_filters.as_list()),
            'offset': search_offset,
            'type': search_result_type,
            'content_types': ','.join(search_content_types) if search_content_types else search_content_types,
        })
    )


def test_query_with_range_filters(
        mock_box_session,
        make_mock_box_request,
        test_search,
        search_query,
        search_limit,
        search_offset,
        search_range_filters,
        search_response,
        search_entries,
        search_result_type,
        search_content_types,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value, _ = make_mock_box_request(response=search_response)
    response = test_search.query(
        search_query,
        limit=search_limit,
        offset=search_offset,
        metadata_filters=search_range_filters,
        result_type=search_result_type,
        content_types=search_content_types,
    )
    for actual, expected in zip(response, [File(mock_box_session, item['id'], item) for item in search_entries]):
        assert actual == expected

    mock_box_session.get.assert_called_once_with(
        test_search.get_url(),
        params=Matcher(compare_params, {
            'query': search_query,
            'limit': search_limit,
            'mdfilters': json.dumps(search_range_filters.as_list()),
            'offset': search_offset,
            'type': search_result_type,
            'content_types': ','.join(search_content_types) if search_content_types else search_content_types,
        })
    )


@pytest.mark.parametrize('kwargs, params', [
    ({'scope': SearchScope.ENTERPRISE}, {'scope': 'enterprise_content'}),
    ({'scope': SearchScope.USER}, {'scope': 'user_content'}),
    ({'created_at_range': (None, '2018-01-01T00:00:00Z')}, {'created_at_range': ',2018-01-01T00:00:00Z'}),
    ({'created_at_range': ('2015-02-03T12:00:00-08:00', None)}, {'created_at_range': '2015-02-03T12:00:00-08:00,'}),
    ({'created_at_range': ('2012-01-01T00:00:00Z', '2012-12-31T11:59:59Z')}, {'created_at_range': '2012-01-01T00:00:00Z,2012-12-31T11:59:59Z'}),
    ({'updated_at_range': (None, '2018-01-01T00:00:00Z')}, {'updated_at_range': ',2018-01-01T00:00:00Z'}),
    ({'updated_at_range': ('2015-02-03T12:00:00-08:00', None)}, {'updated_at_range': '2015-02-03T12:00:00-08:00,'}),
    ({'updated_at_range': ('2012-01-01T00:00:00Z', '2012-12-31T11:59:59Z')}, {'updated_at_range': '2012-01-01T00:00:00Z,2012-12-31T11:59:59Z'}),
    ({'size_range': (None, 123)}, {'size_range': ',123'}),
    ({'size_range': (123, None)}, {'size_range': '123,'}),
    ({'size_range': (123, 456)}, {'size_range': '123,456'}),
    ({'trash_content': TrashContent.NONE}, {'trash_content': 'non_trashed_only'}),
    ({'trash_content': TrashContent.ONLY}, {'trash_content': 'trashed_only'}),
    ({'sort': 'modified_at'}, {'sort': 'modified_at'}),
    ({'direction': 'DESC'}, {'direction': 'DESC'}),
])
def test_query_with_optional_parameters(
        mock_box_session,
        test_search,
        make_mock_box_request,
        search_query,
        search_response,
        search_entries,
        kwargs,
        params
):
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value, _ = make_mock_box_request(response=search_response)
    response = test_search.query(
        search_query,
        **kwargs
    )
    for actual, expected in zip(response, [File(mock_box_session, item['id'], item) for item in search_entries]):
        assert actual == expected

    expected_params = {
        'query': search_query,
    }
    expected_params.update(params)

    mock_box_session.get.assert_called_once_with(
        test_search.get_url(),
        params=Matcher(compare_params, expected_params)
    )


def test_query_with_owner_users(
        mock_box_session,
        test_search,
        make_mock_box_request,
        search_query,
        search_response,
        search_entries,
):
    # pylint:disable=redefined-outer-name
    user1 = User(mock_box_session, '987')
    user2 = User(mock_box_session, '654')
    mock_box_session.get.return_value, _ = make_mock_box_request(response=search_response)
    response = test_search.query(
        search_query,
        owner_users=[user1, user2],
    )
    for actual, expected in zip(response, [File(mock_box_session, item['id'], item) for item in search_entries]):
        assert actual == expected

    mock_box_session.get.assert_called_once_with(
        test_search.get_url(),
        params=Matcher(compare_params, {
            'query': search_query,
            'owner_user_ids': '987,654'
        })
    )


def test_metadata_query(
        mock_box_session,
        make_mock_box_request,
        test_search,
        metadata_query_response
):
    # pylint:disable=redefined-outer-name
    expected_url = f'{API.BASE_API_URL}/metadata_queries/execute_read'
    from_template = 'enterprise_12345.someTemplate'
    ancestor_folder_id = '5555'
    query = 'amount >= :arg'
    query_params = {'arg': 100}
    order_by = [
        {
            'field_key': 'amount',
            'direction': 'asc'
        }
    ]
    fields = ['type', 'id', 'name', 'metadata.enterprise_67890.catalogImages.$parent']
    limit = 2
    marker = 'AAAAAmVYB1FWec8GH6yWu2nwmanfMh07IyYInaa7DZDYjgO1H4KoLW29vPlLY173OKs'
    expected_data = {
        'limit': limit,
        'from': from_template,
        'ancestor_folder_id': ancestor_folder_id,
        'query': query,
        'query_params': query_params,
        'order_by': order_by,
        'marker': marker,
        'fields': fields
    }
    expected_headers = {b'Content-Type': b'application/json'}
    mock_box_session.post.return_value, _ = make_mock_box_request(response=metadata_query_response)
    items = test_search.metadata_query(
        from_template=from_template,
        ancestor_folder_id=ancestor_folder_id,
        query=query,
        query_params=query_params,
        order_by=order_by,
        marker=marker,
        limit=limit,
        fields=fields
    )
    item1 = items.next()
    item2 = items.next()
    mock_box_session.post.assert_called_once_with(expected_url, data=ANY, headers=expected_headers)
    assert dict(json.loads(mock_box_session.post.call_args[1]['data'])) == expected_data
    assert mock_box_session.post.call_args[1]['headers'] == expected_headers
    assert item1['type'] == 'file'
    assert item1['metadata']['enterprise_67890']['catalogImages']['$parent'] == 'file_50347290'
    assert item2['type'] == 'folder'
    assert item2['metadata']['enterprise_67890']['catalogImages']['$parent'] == 'file_50427291'


def test_range_filter_without_gt_and_lt_will_fail_validation():
    metadata_filter = MetadataSearchFilter(template_key='mytemplate', scope='enterprise')
    with pytest.raises(ValueError):
        metadata_filter.add_range_filter(field_key='mykey')


def test_start_search_filters(test_search):
    filters = test_search.start_metadata_filters()
    assert isinstance(filters, MetadataSearchFilters)


def test_make_single_metadata_filter(test_search):
    template_key = 'mytemplate'
    scope = 'myscope'
    metadata_filter = test_search.make_single_metadata_filter(template_key, scope)
    assert isinstance(metadata_filter, MetadataSearchFilter)
    filter_as_dict = metadata_filter.as_dict()
    assert filter_as_dict['templateKey'] == template_key
    assert filter_as_dict['scope'] == scope


def test_query_with_shared_links(
        mock_box_session,
        make_mock_box_request,
        search_content_types,
        search_limit,
        search_offset,
        search_query,
        search_result_type,
        search_value_based_filters,
        search_with_shared_links_entries,
        search_with_shared_links_response,
        test_search,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value, _ = make_mock_box_request(response=search_with_shared_links_response)
    response = test_search.query_with_shared_links(
        search_query,
        limit=search_limit,
        offset=search_offset,
        metadata_filters=search_value_based_filters,
        result_type=search_result_type,
        content_types=search_content_types,
    )

    for actual, expected in zip(response, [File(mock_box_session, entry['item']['id'], entry['item']) for entry in search_with_shared_links_entries]):
        assert actual.item == expected

    mock_box_session.get.assert_called_once_with(
        test_search.get_url(),
        params=Matcher(compare_params, {
            'query': search_query,
            'include_recent_shared_links': True,
            'limit': search_limit,
            'mdfilters': json.dumps(search_value_based_filters.as_list()),
            'offset': search_offset,
            'type': search_result_type,
            'content_types': ','.join(search_content_types) if search_content_types else search_content_types,
        })
    )
