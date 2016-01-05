# coding: utf-8

from __future__ import unicode_literals, absolute_import

import pytest

from boxsdk.util.multipart_stream import MultipartStream


@pytest.fixture(params=({}, {'data_1': b'data_1_value', 'data_2': b'data_2_value'}))
def multipart_stream_data(request):
    return request.param


@pytest.fixture(params=({}, {'file_1': b'file_1_value', 'file_2': b'file_2_value'}))
def multipart_stream_files(request):
    return request.param


def test_multipart_stream_orders_data_before_files(multipart_stream_data, multipart_stream_files):
    # pylint:disable=redefined-outer-name
    if not multipart_stream_data and not multipart_stream_files:
        pytest.xfail('Encoder does not support empty fields.')
    stream = MultipartStream(multipart_stream_data, multipart_stream_files)
    encoded_stream = stream.to_string()
    data_indices = [encoded_stream.find(value) for value in multipart_stream_data.values()]
    file_indices = [encoded_stream.find(value) for value in multipart_stream_files.values()]
    assert -1 not in data_indices
    assert -1 not in file_indices
    assert all((all((data_index < f for f in file_indices)) for data_index in data_indices))
