from datetime import datetime
from typing import Union, Optional

from dateutil import parser


def normalize_date_to_rfc3339_format(date: Union[None, datetime, str]) -> Optional[str]:
    """
    Normalizes any datetime string supported by dateutil library or a datetime.datetime object to rfc3339 format.

    :param date:  datetime str or datetime object
    :return: date-time str in rfc3339 format
    """
    if date is None:
        return None

    if isinstance(date, str):
        date = parser.parse(date)

    if not isinstance(date, datetime):
        raise TypeError(f"Got unsupported type {date.__class__.__name__!r} for date.")

    timezone_aware_datetime = date if date.tzinfo is not None else date.astimezone()
    return timezone_aware_datetime.isoformat(timespec='seconds')
