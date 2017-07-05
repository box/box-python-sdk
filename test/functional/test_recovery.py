# coding: utf-8

from __future__ import unicode_literals
import pytest
from boxsdk.exception import BoxAPIException
from test.functional.mock_box.util.chaos_utils import error, html, xml
from test.functional.mock_box.util.http_utils import RETRY_AFTER_HEADER


@pytest.fixture(params=[500, 501])
def error_code(request):
    return request.param


@pytest.fixture(params=[202, 429])
def retry_code(request):
    return request.param


@pytest.fixture(autouse=True)
def mock_sleep(monkeypatch):
    monkeypatch.setattr('time.sleep', lambda seconds: None)


@pytest.fixture(params=[1, 2, (1, 2), (1, 3)])
def should_apply(request):
    expected_num_requests = 4  # 3 auth requests and 1 folder info request
    # Figure out how many times the call should fail. If should_apply is an int, it should fail iff should_apply == 1
    # If it's a sequence, figure out the first time it will succeed. It should fail until then.
    if isinstance(request.param, int):
        if request.param is 1:
            expected_num_requests += 1
    else:
        expected_num_requests += next(
            (a for a in enumerate(sorted(request.param)) if a[0] + 1 != a[1]),
            [0],
        )[0] or len(request.param)
    return request.param, expected_num_requests


@pytest.fixture(autouse=True)
def reset_chaos(mock_box, request):
    mock_box.get_folder_info.reset_chaos()
    request.addfinalizer(mock_box.get_folder_info.reset_chaos)


def test_client_retries_on_server_error(box_client, mock_box, error_code, should_apply):
    # pylint:disable=redefined-outer-name
    should_apply, expected_num_requests = should_apply
    mock_box.get_folder_info.add_chaos(error(error_code), should_apply)
    box_client.folder('0').get()
    assert len(mock_box.requests) == expected_num_requests


def test_client_retries_on_retry_after(box_client, mock_box, retry_code, should_apply):
    # pylint:disable=redefined-outer-name
    should_apply, expected_num_requests = should_apply
    mock_box.get_folder_info.add_chaos(error(retry_code, headers={RETRY_AFTER_HEADER: 1}), should_apply)
    box_client.folder('0').get()
    assert len(mock_box.requests) == expected_num_requests


def test_client_stops_retrying_after_10_server_errors(box_client, mock_box, error_code):
    # pylint:disable=redefined-outer-name
    mock_box.get_folder_info.add_chaos(error(error_code))
    with pytest.raises(BoxAPIException) as exc_info:
        box_client.folder('0').get()
        assert exc_info.value.status == error_code
    assert len(mock_box.requests) == 14  # 3 auth requests, 1 try, and 10 retries


@pytest.mark.parametrize('chaos', [html, xml])
def test_non_json_response_raises(box_client, mock_box, chaos):
    # pylint:disable=redefined-outer-name
    mock_box.get_folder_info.add_chaos(chaos)
    with pytest.raises(BoxAPIException) as exc_info:
        box_client.folder('0').get()
        assert exc_info.value.status == 200
        assert 'json' in exc_info.value.message


def test_unknown_resource_raises(box_client):
    folder = box_client.folder('0')
    with pytest.raises(BoxAPIException) as exc_info:
        # pylint:disable=protected-access
        box_client.make_request('get', folder.get_url('unknown')).get_info()
        # pylint:enable=protected-access
        assert exc_info.value.status == 404


def test_make_request_equivalent_to_get_items(box_client):
    folder = box_client.folder('0')
    # pylint:disable=protected-access
    response = box_client.make_request('get', folder.get_url())
    # pylint:enable=protected-access
    assert response.status_code == 200
