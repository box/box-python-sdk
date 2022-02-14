from unittest.mock import mock_open


def streamable_mock_open(mock=None, read_data=b''):
    mock = mock_open(mock, read_data)
    handle = mock.return_value
    handle.position = 0

    def tell():
        return handle.position

    def read(size=-1):
        if size == -1:
            handle.position = len(read_data)
            return read_data

        data = read_data[handle.position:handle.position + size]
        handle.position += size
        return data

    # pylint:disable=no-member
    handle.tell.side_effect = tell
    handle.len = len(read_data)
    handle.read.side_effect = read
    del handle.getvalue
    return mock
