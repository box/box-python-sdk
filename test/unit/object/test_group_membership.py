# coding: utf-8

from __future__ import unicode_literals
import pytest

from boxsdk.object.group_membership import GroupMembership
from boxsdk.object.group import Group
from boxsdk.object.user import User


@pytest.fixture(params=[True, False])
def mock_group_membership_dict_or_none(request, mock_group_membership_dict):
    return mock_group_membership_dict if request.param else None


@pytest.fixture(params=[True, False])
def mock_user_and_group_or_none(request, mock_user, mock_group):
    return (mock_user, mock_group) if request.param else None


def test_group_membership_initialization(
        mock_box_session,
        mock_group_membership_dict_or_none,
        mock_user_and_group_or_none,
):
    # pylint:disable=redefined-outer-name
    fake_id = "fake_membership_id"
    response_object = mock_group_membership_dict_or_none

    kwargs = {}

    if mock_user_and_group_or_none:
        kwargs['user'], kwargs['group'] = mock_user_and_group_or_none
        user_id, group_id = kwargs['user'].object_id, kwargs['group'].object_id
    else:
        user_id, group_id = None, None

    group_membership = GroupMembership(mock_box_session, fake_id, response_object, **kwargs)

    assert group_membership.object_id == fake_id

    # pylint:disable=protected-access
    assert group_membership._session == mock_box_session
    if response_object:
        assert group_membership._response_object is response_object
    else:
        assert not group_membership._response_object
    # pylint:enable=protected-access

    _assert_object_is_valid(group_membership.user, bool(response_object), user_id, User, kwargs.get('user'))
    _assert_object_is_valid(group_membership.group, bool(response_object), group_id, Group, kwargs.get('group'))


def _assert_object_is_valid(actual_object, has_response, object_id, expected_class, expected_object):
    if has_response or object_id:
        assert isinstance(actual_object, expected_class)
    else:
        assert actual_object is None
    if object_id:
        assert actual_object is expected_object
