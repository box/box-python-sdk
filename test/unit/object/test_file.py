# coding: utf-8

from __future__ import unicode_literals
import json
from mock import mock_open, patch
import pytest
from six import BytesIO
from boxsdk.config import API
from boxsdk.exception import BoxAPIException
from boxsdk.object.file import File


# pylint:disable=protected-access
# pylint:disable=redefined-outer-name

@pytest.fixture()
def mock_accelerator_upload_url_for_update():
    return 'https://upload.box.com/api/2.0/files/fake_file_id/content?upload_session_id=123'


@pytest.fixture(scope='function')
def mock_accelerator_response_for_update(make_mock_box_request, mock_accelerator_upload_url_for_update):
    mock_response, _ = make_mock_box_request(
        response={
            'upload_url': mock_accelerator_upload_url_for_update,
            'download_url': None,
        }
    )
    return mock_response


def test_delete_file(test_file, mock_box_session, etag, if_match_header):
    test_file.delete(etag=etag)
    expected_url = test_file.get_url()
    mock_box_session.delete.assert_called_once_with(
        expected_url,
        expect_json_response=False,
        params={},
        headers=if_match_header,
    )


def test_download_to(test_file, mock_box_session, mock_content_response):
    expected_url = test_file.get_url('content')
    mock_box_session.get.return_value = mock_content_response
    mock_writeable_stream = BytesIO()
    test_file.download_to(mock_writeable_stream)
    mock_writeable_stream.seek(0)
    assert mock_writeable_stream.read() == mock_content_response.content
    mock_box_session.get.assert_called_once_with(expected_url, expect_json_response=False, stream=True)


def test_get_content(test_file, mock_box_session, mock_content_response):
    expected_url = test_file.get_url('content')
    mock_box_session.get.return_value = mock_content_response
    file_content = test_file.content()
    assert file_content == mock_content_response.content
    mock_box_session.get.assert_called_once_with(expected_url, expect_json_response=False)


@pytest.mark.parametrize('is_stream', (True, False))
def test_update_contents(
        test_file,
        mock_box_session,
        mock_content_response,
        mock_upload_response,
        mock_file_path,
        etag,
        upload_using_accelerator,
        mock_accelerator_response_for_update,
        mock_accelerator_upload_url_for_update,
        upload_using_accelerator_fails,
        if_match_header,
        is_stream,
):
    expected_url = test_file.get_url('content').replace(API.BASE_API_URL, API.UPLOAD_URL)
    if upload_using_accelerator:
        if upload_using_accelerator_fails:
            mock_box_session.options.side_effect = BoxAPIException(400)
        else:
            mock_box_session.options.return_value = mock_accelerator_response_for_update
            expected_url = mock_accelerator_upload_url_for_update

    mock_box_session.post.return_value = mock_upload_response

    if is_stream:
        mock_file_stream = BytesIO(mock_content_response.content)
        new_file = test_file.update_contents_with_stream(
            mock_file_stream,
            etag=etag,
            upload_using_accelerator=upload_using_accelerator,
        )
    else:
        mock_file = mock_open(read_data=mock_content_response.content)
        mock_file_stream = mock_file.return_value
        with patch('boxsdk.object.file.open', mock_file, create=True):
            new_file = test_file.update_contents(
                mock_file_path,
                etag=etag,
                upload_using_accelerator=upload_using_accelerator,
            )

    mock_files = {'file': ('unused', mock_file_stream)}
    mock_box_session.post.assert_called_once_with(
        expected_url,
        expect_json_response=False,
        files=mock_files,
        headers=if_match_header,
    )
    assert isinstance(new_file, File)
    assert new_file.object_id == mock_upload_response.json()['entries'][0]['id']


def test_update_contents_with_stream_does_preflight_check_if_specified(
        test_file,
        preflight_check,
        file_size,
        preflight_fails,
        mock_box_session,
):
    with patch.object(File, 'preflight_check', return_value=None):
        kwargs = {'file_stream': BytesIO(b'some bytes')}
        if preflight_check:
            kwargs['preflight_check'] = preflight_check
            kwargs['preflight_expected_size'] = file_size
        if preflight_fails:
            test_file.preflight_check.side_effect = BoxAPIException(400)
            with pytest.raises(BoxAPIException):
                test_file.update_contents_with_stream(**kwargs)
        else:
            test_file.update_contents_with_stream(**kwargs)

        if preflight_check:
            assert test_file.preflight_check.called_once_with(size=file_size)
            if preflight_fails:
                assert not mock_box_session.post.called
            else:
                assert mock_box_session.post.called
        else:
            assert not test_file.preflight_check.called


@patch('boxsdk.object.file.open', mock_open(read_data=b'some bytes'), create=True)
def test_update_contents_does_preflight_check_if_specified(
        test_file,
        mock_file_path,
        preflight_check,
        file_size,
        preflight_fails,
        mock_box_session,
):
    with patch.object(File, 'preflight_check', return_value=None):
        kwargs = {'file_path': mock_file_path}
        if preflight_check:
            kwargs['preflight_check'] = preflight_check
            kwargs['preflight_expected_size'] = file_size
        if preflight_fails:
            test_file.preflight_check.side_effect = BoxAPIException(400)
            with pytest.raises(BoxAPIException):
                test_file.update_contents(**kwargs)
        else:
            test_file.update_contents(**kwargs)

        if preflight_check:
            assert test_file.preflight_check.called_once_with(size=file_size)
            if preflight_fails:
                assert not mock_box_session.post.called
            else:
                assert mock_box_session.post.called
        else:
            assert not test_file.preflight_check.called


@pytest.mark.parametrize('prevent_download', (True, False))
def test_lock(test_file, mock_box_session, mock_file_response, prevent_download):
    expected_url = test_file.get_url()
    mock_box_session.put.return_value = mock_file_response
    test_file.lock(prevent_download)
    mock_box_session.put.assert_called_once_with(
        expected_url,
        data=json.dumps({'lock': {'is_download_prevented': prevent_download, 'type': 'lock'}}),
        params=None,
        headers=None,
    )


def test_unlock(test_file, mock_box_session, mock_file_response):
    expected_url = test_file.get_url()
    mock_box_session.put.return_value = mock_file_response
    test_file.unlock()
    mock_box_session.put.assert_called_once_with(
        expected_url,
        data=json.dumps({'lock': None}),
        params=None,
        headers=None,
    )


@pytest.mark.parametrize(
    'size, name, expected_data',
    [
        # Test case for specifying the name of the file for preflight
        (
            100,
            'foo.txt',
            json.dumps({'size': 100, 'name': 'foo.txt'}),
        ),

        # Test case for omitting the name of the file for preflight
        (
            200,
            None,
            json.dumps({'size': 200})
        ),
    ]
)
def test_preflight_check(
        test_file,
        mock_object_id,
        mock_box_session,
        size,
        name,
        expected_data,
):
    kwargs = {'size': size}
    if name:
        kwargs['name'] = name
    test_file.preflight_check(**kwargs)
    mock_box_session.options.assert_called_once_with(
        url='{0}/files/{1}/content'.format(
            API.BASE_API_URL,
            mock_object_id,
        ),
        expect_json_response=False,
        data=expected_data,
    )


def test_get_shared_link_download_url(
        test_file,
        mock_box_session,
        shared_link_access,
        shared_link_unshared_at,
        shared_link_password,
        shared_link_can_preview,
        test_url,
        etag,
        if_match_header,
):
    # pylint:disable=redefined-outer-name, protected-access
    expected_url = test_file.get_url()
    mock_box_session.put.return_value.json.return_value = {'shared_link': {'url': None, 'download_url': test_url}}
    expected_data = {'shared_link': {}}
    if shared_link_access is not None:
        expected_data['shared_link']['access'] = shared_link_access
    if shared_link_unshared_at is not None:
        expected_data['shared_link']['unshared_at'] = shared_link_unshared_at.isoformat()
    if shared_link_can_preview is not None:
        expected_data['shared_link']['permissions'] = permissions = {}
        permissions['can_preview'] = shared_link_can_preview
    if shared_link_password is not None:
        expected_data['shared_link']['password'] = shared_link_password
    url = test_file.get_shared_link_download_url(
        etag=etag,
        access=shared_link_access,
        unshared_at=shared_link_unshared_at,
        password=shared_link_password,
        allow_preview=shared_link_can_preview,
    )
    mock_box_session.put.assert_called_once_with(
        expected_url,
        data=json.dumps(expected_data),
        headers=if_match_header,
        params=None,
    )
    assert url == test_url
