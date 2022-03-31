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
        lazy_fixture("mock_datetime_rfc3339_str"),
    ),
)
def test_leave_datetime_string_unchanged_when_rfc3339_formatted_str_provided(
    valid_datetime_format,
):
    formatted_str = datetime_formatter.normalize_date_to_rfc3339_format(
        valid_datetime_format
    )
    assert formatted_str == valid_datetime_format


@pytest.mark.parametrize(
    "other_datetime_format",
    (
        "2035-03-04T10:14:24.000+14:00",
        "2035-03-04 10:14:24.000+14:00",
        "2035/03/04 10:14:24.000+14:00",
        "2035/03/04T10:14:24+14:00",
        "2035/3/4T10:14:24+14:00",
        lazy_fixture('mock_timezone_aware_datetime_obj'),
    ),
)
def test_normalize_date_to_rfc3339_format_timezone_aware_datetime(
    other_datetime_format,
    mock_datetime_rfc3339_str,
):
    formatted_str = datetime_formatter.normalize_date_to_rfc3339_format(
        other_datetime_format
    )
    assert formatted_str == mock_datetime_rfc3339_str


@pytest.mark.parametrize(
    "timezone_naive_datetime",
    (
        "2035-03-04T10:14:24.000",
        "2035-03-04T10:14:24",
        lazy_fixture('mock_timezone_naive_datetime_obj')
    ),
)
def test_add_timezone_info_when_timezone_naive_datetime_provided(
    timezone_naive_datetime,
    mock_timezone_naive_datetime_obj,
):
    formatted_str = datetime_formatter.normalize_date_to_rfc3339_format(
        timezone_naive_datetime
    )

    local_timezone = datetime.datetime.now().tzinfo
    expected_datetime = mock_timezone_naive_datetime_obj.astimezone(
        tz=local_timezone
    ).isoformat(timespec="seconds")
    assert formatted_str == expected_datetime


def test_return_none_when_none_provided():
    assert datetime_formatter.normalize_date_to_rfc3339_format(None) is None


@pytest.mark.parametrize("inavlid_datetime_object", (Mock(),))
def test_throw_type_error_when_invalid_datetime_object_provided(
    inavlid_datetime_object,
):
    with pytest.raises(TypeError):
        datetime_formatter.normalize_date_to_rfc3339_format(inavlid_datetime_object)
