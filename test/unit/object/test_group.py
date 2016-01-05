# coding: utf-8

from __future__ import unicode_literals

from itertools import chain, islice, repeat, count
import json
from operator import sub

from mock import Mock
import pytest
from six.moves import map  # pylint:disable=redefined-builtin,import-error

from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.object.group_membership import GroupMembership
from boxsdk.config import API
from boxsdk.session.box_session import BoxResponse


@pytest.fixture(scope='module')
def delete_group_response():
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.ok = True
    return mock_network_response


def test_delete_group_return_the_correct_response(
        mock_group,
        mock_box_session,
        delete_group_response,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.delete.return_value = delete_group_response
    response = mock_group.delete()

    # pylint:disable=protected-access
    expected_url = mock_group.get_url()
    # pylint:enable=protected-access
    mock_box_session.delete.assert_called_once_with(expected_url, params={}, expect_json_response=False, headers=None)

    assert response is True


@pytest.mark.parametrize('role', ['member', 'admin'])
def test_add_member(test_group, mock_box_session, mock_add_member_response, mock_user, role):
    expected_url = '{0}/group_memberships'.format(API.BASE_API_URL)
    mock_box_session.post.return_value = mock_add_member_response
    new_group_membership = test_group.add_member(mock_user, role)
    data = json.dumps({
        'user': {'id': mock_user.object_id},
        'group': {'id': test_group.object_id},
        'role': role,
    })
    mock_box_session.post.assert_called_once_with(expected_url, data=data)
    assert isinstance(new_group_membership, GroupMembership)


@pytest.fixture()
def mock_membership_dict_stream():
    def gen_data(some_id):
        return {
            'type': 'group_membership',
            'id': "membership_id_{0}".format(some_id),
            'role': 'member',
            'user': {'type': 'user', 'id': "user_id_{0}".format(some_id)},
            'group': {'type': 'group', 'id': "group_id_{0}".format(some_id)},
        }

    return map(gen_data, count())


@pytest.fixture()
def mock_membership_responses(mock_membership_dict_stream):
    """
    Returns a generator method that takes params: total, page_size.
    The generator generates a sequence of 'group membership' mock_box_responses each containing page_size
    items, until 'total' entries have been returned
    """
    # pylint:disable=redefined-outer-name
    def number_entries_per_response(total, page_size, hidden_in_batch):
        if not hidden_in_batch:
            hidden_in_batch = repeat(0)
        quotient, remainder = divmod(total, page_size)
        max_items_in_batch = chain(repeat(page_size, quotient), (remainder,))
        return map(sub, max_items_in_batch, hidden_in_batch)

    def take(iterable, number):
        return list(islice(iterable, number))

    def membership_responses(total, page_size, hidden_in_batch=None):
        offset = 0
        for number_entries in number_entries_per_response(total, page_size, hidden_in_batch):
            entries = take(mock_membership_dict_stream, number_entries)

            mock_box_response = Mock(BoxResponse)
            mock_network_response = Mock(DefaultNetworkResponse)
            mock_box_response.network_response = mock_network_response
            mock_box_response.json.return_value = {
                'entries': entries,
                'total_count': total,
                'offset': offset,
                'limit': page_size,
            }
            offset += number_entries
            mock_box_response.status_code = 200
            mock_box_response.ok = True
            yield mock_box_response

    return membership_responses


@pytest.mark.parametrize('total, page_size', [
    (0, 6),
    (5, 6),
    (6, 6),
    (5, 4),
    (9, 4),
])
def test_membership(test_group, mock_box_session, mock_membership_responses, total, page_size):
    # pylint:disable=redefined-outer-name
    # Each call the 'get' (the GET next page call) will return the next response
    mock_box_session.get.side_effect = mock_membership_responses(total, page_size)

    # Get all the members
    all_members = list(test_group.membership(0, page_size))

    # Assert we got the expected number of membership instances
    assert len(all_members) == total
    assert all(isinstance(m, GroupMembership) for m in all_members)


@pytest.mark.parametrize('hidden_in_batch', [
    (1, 0, 0),
    (0, 0, 1),
    (10, 10, 9),
    (10, 10, 10),
])
def test_membership_with_hidden_results(test_group, mock_box_session, mock_membership_responses, hidden_in_batch):
    """
    This test verifies that the SDK properly deals with missing (aka hidden) data potentially present in a paged
    API. The API might indicate that the total_size is X, but in actuality the pages API could return less than X
    because the auth'd user might not have access to all X of the resources.
    """
    # pylint:disable=redefined-outer-name
    total = 30
    page_size = 10

    total_hidden = sum(hidden_in_batch)

    # Each call the 'get' (the GET next page call) will return the next response
    mock_box_session.get.side_effect = mock_membership_responses(total, page_size, hidden_in_batch=hidden_in_batch)

    # Get all the members
    all_members = list(test_group.membership(0, page_size))

    # Assert we got the expected number of membership instances
    assert len(all_members) == total - total_hidden
    assert all(isinstance(m, GroupMembership) for m in all_members)


def test_membership_with_page_info(test_group, mock_box_session, mock_membership_responses):
    """
    Verify that the paging info returned by the membership call when include_page_info=True
    is correct, thus allowing a client complete knowledge of when another API call
    is going to be triggered.
    """
    # pylint:disable=redefined-outer-name
    total = 9
    page_size = 3
    hidden_in_batch = 0, 2, 1

    # Each call to 'get' (the GET next page call) will return the next response
    mock_box_session.get.side_effect = mock_membership_responses(total, page_size, hidden_in_batch=hidden_in_batch)

    # Initialize the generator of all the membership
    group_generator = test_group.membership(0, page_size, include_page_info=True)

    # manually get all the items, verifying that the page-info data is correct.
    _, page_size, index = next(group_generator)
    assert page_size == 3 and index == 0
    _, page_size, index = next(group_generator)
    assert page_size == 3 and index == 1
    _, page_size, index = next(group_generator)
    assert page_size == 3 and index == 2

    # This next call will trigger a new GET request, returning the 2nd page
    _, page_size, index = next(group_generator)
    assert page_size == 1 and index == 0

    # This next call will trigger a new GET request, returning the 3rd page
    _, page_size, index = next(group_generator)
    assert page_size == 2 and index == 0
    _, page_size, index = next(group_generator)
    assert page_size == 2 and index == 1

    with pytest.raises(StopIteration):
        next(group_generator)
