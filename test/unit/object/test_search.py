# coding: utf-8

from __future__ import unicode_literals

import json

import pytest

from boxsdk.object.file import File
from boxsdk.object.search import MetadataSearchFilters, MetadataSearchFilter


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
    return {
        'entries': search_entries(),
        'total_count': 0,
        'limit': 20,
        'offset': 0
    }


class Matcher(object):
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


def test_search_with_value_based_filters(
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
    response = test_search.search(
        search_query,
        limit=search_limit,
        offset=search_offset,
        metadata_filters=search_value_based_filters,
        result_type=search_result_type,
        content_types=search_content_types,
    )
    assert response == [File(mock_box_session, search_entry['id'], search_entry) for search_entry in search_entries]

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


def test_search_with_range_filters(
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
    response = test_search.search(
        search_query,
        limit=search_limit,
        offset=search_offset,
        metadata_filters=search_range_filters,
        result_type=search_result_type,
        content_types=search_content_types,
    )
    assert response == [File(mock_box_session, search_entry['id'], search_entry) for search_entry in search_entries]

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
