# coding: utf-8

from __future__ import unicode_literals
import pytest
import json
from boxsdk.object.file import File
from boxsdk.object.search import MetadataSearchFilters, MetadataSearchFilter

@pytest.fixture
def search_query():
    return 'myquery'

@pytest.fixture
def search_limit():
    return 20

@pytest.fixture
def search_offset():
    return 0

@pytest.fixture
def search_value_based_mdfilters():
    mdfilters = MetadataSearchFilters()
    mdfilter = MetadataSearchFilter('properties', 'global')
    mdfilter.add_value_based_filter('myfield', 'myvalue')
    mdfilters.add_filter(mdfilter)
    return mdfilters

@pytest.fixture(params=({'gt_value':'mygtvalue'},{'lt_value':'myltvalue'},{'gt_value':'mygtvalue','lt_value':'myltvalue'}))
def search_range_mdfilters(request):
    mdfilters = MetadataSearchFilters()
    mdfilter = MetadataSearchFilter('properties', 'global')
    filter_params = {'field_key': 'myfield'}
    filter_params.update(request.param)
    mdfilter.add_range_filter(**filter_params)
    mdfilters.add_filter(mdfilter)
    return mdfilters

@pytest.fixture
def search_entries():
    return [
        {'id': '1234', 'type': 'file'}
    ]

@pytest.fixture
def search_response(search_entries):
    return {
        'entries': search_entries,
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
    if not type(self) == type(other):
        return False
    for key in self:
        # We need to ensure that the JSON-encoded mdfilters matches regardless of key order
        if key == 'mdfilters':
            if json.loads(self['mdfilters']) != json.loads(other['mdfilters']):
                return False
        # For other keys, just ensure that they are equal
        else:
            if self[key] != other[key]:
                return False
    return True


def test_search_with_value_based_mdfilters(
        mock_box_session,
        make_mock_box_request,
        test_search,
        search_query,
        search_limit,
        search_offset,
        search_value_based_mdfilters,
        search_response,
        search_entries
):
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value, _ = make_mock_box_request(response=search_response)
    response = test_search.search(search_query, limit=search_limit, offset=search_offset, mdfilters=search_value_based_mdfilters)
    assert response == [File(mock_box_session, search_entry['id'], search_entry) for search_entry in search_entries]

    mock_box_session.get.assert_called_once_with(
        test_search.get_url(),
        params=Matcher(compare_params, {'query': 'myquery', 'limit': 20, 'mdfilters': json.dumps(search_value_based_mdfilters.as_list()), 'offset': 0})
    )

def test_search_with_range_mdfilters(
        mock_box_session,
        make_mock_box_request,
        test_search,
        search_query,
        search_limit,
        search_offset,
        search_range_mdfilters,
        search_response,
        search_entries
):
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value, _ = make_mock_box_request(response=search_response)
    response = test_search.search(search_query, limit=search_limit, offset=search_offset, mdfilters=search_range_mdfilters)
    assert response == [File(mock_box_session, search_entry['id'], search_entry) for search_entry in search_entries]

    mock_box_session.get.assert_called_once_with(
        test_search.get_url(),
        params=Matcher(compare_params, {'query': 'myquery', 'limit': 20, 'mdfilters': json.dumps(search_range_mdfilters.as_list()), 'offset': 0})
    )
