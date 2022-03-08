from datetime import datetime
from typing import Union


def normalize_date_to_rfc3339_format(date: Union[datetime, str]) -> str:
    """
    :param date:  datetime str or datetime object
    :return: date-time str in rfc3339 format
    """
    if isinstance(date, str):
        datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
        return date
    if isinstance(date, datetime):
        timezone_aware_datetime = date if date.tzinfo is not None else date.astimezone()
        return timezone_aware_datetime.isoformat(timespec='seconds')
    raise TypeError(f"Got unsupported type {date.__class__.__name__!r} for date.")
