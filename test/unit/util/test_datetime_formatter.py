from unittest.mock import Mock

import datetime
import pytest

from pytest_lazyfixture import lazy_fixture

from boxsdk.util import datetime_formatter


@pytest.mark.parametrize(
    "valid_datetime_format",
    (
        "2035-03-04T10:14:24+14:00",
        "2035-03-04T10:14:24-04:00",
        "2035-03-04T10:14:24Z",
        lazy_fixture("mock_datetime_rfc3339_str"),
    ),
)
def test_normalize_date_to_rfc3339_format_when_valid_datetime_format_provided(
    valid_datetime_format,
):
    formatted_str = datetime_formatter.normalize_date_to_rfc3339_format(
        valid_datetime_format
    )
    assert formatted_str == valid_datetime_format


def test_normalize_date_to_rfc3339_format_when_valid_timezone_aware_datetime_object_provided(
    mock_timezone_aware_datetime_obj, mock_datetime_rfc3339_str
):
    formatted_str = datetime_formatter.normalize_date_to_rfc3339_format(
        mock_timezone_aware_datetime_obj
    )
    assert formatted_str == mock_datetime_rfc3339_str


def test_normalize_date_to_rfc3339_format_when_valid_timezone_naive_datetime_object_provided(
    mock_timezone_naive_datetime_obj,
):
    formatted_str = datetime_formatter.normalize_date_to_rfc3339_format(
        mock_timezone_naive_datetime_obj
    )
    local_timezone = datetime.datetime.now().tzinfo
    expected_datetime = mock_timezone_naive_datetime_obj.astimezone(
        tz=local_timezone
    ).isoformat(timespec="seconds")
    assert formatted_str == expected_datetime


@pytest.mark.parametrize("inavlid_datetime_object", (None, Mock()))
def test_throw_type_error_when_invalid_datetime_object_provided(
    inavlid_datetime_object,
):
    with pytest.raises(TypeError):
        datetime_formatter.normalize_date_to_rfc3339_format(inavlid_datetime_object)
