from io import BytesIO

import pytest

from boxsdk.util.multipart_stream import MultipartStream


@pytest.fixture(params=({}, {'data_1': b'data_1_value', 'data_2': b'data_2_value'}))
def multipart_stream_data(request):
    return request.param


@pytest.fixture(params=({}, {'file_1': b'file_1_value', 'file_2': b'file_2_value'}))
def multipart_stream_files(request):
    return request.param


def test_multipart_stream_orders_data_before_files(
    multipart_stream_data, multipart_stream_files
):
    # pylint:disable=redefined-outer-name
    stream = MultipartStream(multipart_stream_data, multipart_stream_files)
    encoded_stream = stream.read()
    data_indices = [
        encoded_stream.find(value) for value in multipart_stream_data.values()
    ]
    file_indices = [
        encoded_stream.find(value) for value in multipart_stream_files.values()
    ]
    assert -1 not in data_indices
    assert -1 not in file_indices
    assert all(all(data_index < f for f in file_indices) for data_index in data_indices)
    assert len(encoded_stream) == stream.len


def test_multipart_stream_encodes_data_and_file_tuples():
    stream = MultipartStream(
        {'attributes': '{"name": "test_file"}'},
        {
            'file': ('unused', BytesIO(b'file content')),
            'pic': ('avatar.png', BytesIO(b'png bytes'), 'image/png'),
        },
    )

    assert stream.content_type == f'multipart/form-data; boundary={stream.boundary}'
    assert (
        stream.read()
        == (
            f'--{stream.boundary}\r\n'
            'Content-Disposition: form-data; name="attributes"\r\n\r\n'
            '{"name": "test_file"}\r\n'
            f'--{stream.boundary}\r\n'
            'Content-Disposition: form-data; name="file"; filename="unused"\r\n\r\n'
            'file content\r\n'
            f'--{stream.boundary}\r\n'
            'Content-Disposition: form-data; name="pic"; filename="avatar.png"\r\n'
            'Content-Type: image/png\r\n\r\n'
            'png bytes\r\n'
            f'--{stream.boundary}--\r\n'
        ).encode()
    )


def test_multipart_stream_reads_file_lazily():
    file_stream = BytesIO(b'file content')
    file_stream.read(5)

    stream = MultipartStream({}, {'file': ('unused', file_stream)})

    assert file_stream.tell() == 5
    assert b'\r\n\r\ncontent\r\n' in stream.read()
