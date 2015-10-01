# coding: utf-8

from __future__ import unicode_literals
from datetime import datetime, timedelta
import pytest
from boxsdk.util.compat import total_seconds


@pytest.fixture(params=(
    (timedelta(seconds=7), 7),
    (datetime(2015, 7, 6, 12) - datetime(2015, 7, 6, 11), 60 * 60),
    (timedelta(minutes=1), 60),
))
def total_seconds_data(request):
    return request.param


def test_total_seconds(total_seconds_data):
    # pylint:disable=redefined-outer-name
    delta, seconds = total_seconds_data
    assert total_seconds(delta) == seconds
