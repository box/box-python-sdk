# coding: utf-8
import json

from boxsdk.config import API
from boxsdk.object.web_link import WebLink
from boxsdk.util.default_arg_value import SDK_VALUE_NOT_SET


def test_get(mock_box_session, test_web_link):
    # pylint:disable=redefined-outer-name, protected-access
    web_link_id = test_web_link.object_id
    expected_url = f'{API.BASE_API_URL}/web_links/{web_link_id}'
    mock_web_link = {
        'type': 'web_link',
        'url': 'https://test/com',
        'id': 1234,
        'created_at': '2015-05-07T15:00:01-07:00',
    }
    mock_box_session.get.return_value.json.return_value = mock_web_link
    web_link = test_web_link.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert web_link.id == mock_web_link['id']
    assert web_link.type == mock_web_link['type']
    assert web_link.url == mock_web_link['url']
    assert isinstance(web_link, WebLink)


def test_update(mock_box_session, test_web_link):
    # pylint:disable=redefined-outer-name, protected-access
    web_link_id = test_web_link.object_id
    expected_url = f'{API.BASE_API_URL}/web_links/{web_link_id}'
    mock_web_link = {
        'type': 'web_link',
        'url': 'https://newtest.com',
        'id': 1234,
        'created_at': '2015-05-07T15:00:01-07:00',
    }
    data = {
        'url': 'https://newtest.com',
    }
    mock_box_session.put.return_value.json.return_value = mock_web_link
    web_link = test_web_link.update_info(data=data)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(data), headers=None, params=None)
    assert web_link.id == mock_web_link['id']
    assert web_link.type == mock_web_link['type']
    assert web_link.url == mock_web_link['url']
    assert isinstance(web_link, WebLink)


def test_delete(mock_box_session, test_web_link):
    web_link_id = test_web_link.object_id
    expected_url = f'{API.BASE_API_URL}/web_links/{web_link_id}'
    test_web_link.delete()
    mock_box_session.delete.assert_called_once_with(expected_url, expect_json_response=False, headers=None, params={})


def test_get_shared_link(
        test_web_link,
        mock_box_session,
        shared_link_access,
        shared_link_unshared_at,
        shared_link_password,
        shared_link_vanity_name,
        test_url,
):
    # pylint:disable=redefined-outer-name, protected-access
    expected_url = test_web_link.get_url()
    mock_box_session.put.return_value.json.return_value = {
        'type': test_web_link.object_type,
        'id': test_web_link.object_id,
        'shared_link': {
            'url': test_url,
        },
    }
    expected_data = {'shared_link': {}}
    if shared_link_access is not None:
        expected_data['shared_link']['access'] = shared_link_access
    if shared_link_unshared_at is not SDK_VALUE_NOT_SET:
        expected_data['shared_link']['unshared_at'] = shared_link_unshared_at
    if shared_link_password is not None:
        expected_data['shared_link']['password'] = shared_link_password
    if shared_link_vanity_name is not None:
        expected_data['shared_link']['vanity_name'] = shared_link_vanity_name

    url = test_web_link.get_shared_link(
        access=shared_link_access,
        unshared_at=shared_link_unshared_at,
        password=shared_link_password,
        vanity_name=shared_link_vanity_name,
    )
    mock_box_session.put.assert_called_once_with(
        expected_url,
        data=json.dumps(expected_data),
        headers=None,
        params=None,
    )
    assert url == test_url


def test_clear_unshared_at_for_shared_link(
        test_web_link,
        mock_box_session,
        test_url,
):
    expected_url = test_web_link.get_url()
    mock_box_session.put.return_value.json.return_value = {
        'type': test_web_link.object_type,
        'id': test_web_link.object_id,
        'shared_link': {
            'url': test_url,
            'unshared_at': None,
        },
    }
    expected_data = {'shared_link': {'unshared_at': None, }, }
    shared_link = test_web_link.get_shared_link(unshared_at=None)
    mock_box_session.put.assert_called_once_with(
        expected_url,
        data=json.dumps(expected_data),
        headers=None,
        params=None,
    )
    assert shared_link is test_url


def test_remove_shared_link(test_web_link, mock_box_session):
    # pylint:disable=redefined-outer-name, protected-access
    expected_url = test_web_link.get_url()
    mock_box_session.put.return_value.json.return_value = {
        'type': test_web_link.object_type,
        'id': test_web_link.object_id,
        'shared_link': None,
    }
    removed = test_web_link.remove_shared_link()
    mock_box_session.put.assert_called_once_with(
        expected_url,
        data=json.dumps({'shared_link': None}),
        headers=None,
        params=None,
    )
    assert removed is True
