import datetime
import re


RGX_HH_MM = re.compile(r"([0-2]?[0-9]):([0-5][0-9])")
EOD = datetime.time(23, 59, 59)


def add_time(
    start_time: datetime.time, time_delta: datetime.timedelta
) -> datetime.time:
    """Add a timedelta to a datetime.time."""
    start_datetime = datetime.datetime(
        2000,
        1,
        1,
        start_time.hour,
        start_time.minute,
        start_time.second,
        start_time.microsecond,
    )
    end_datetime = start_datetime + time_delta
    return end_datetime.time()


def parse_time(input: str) -> datetime.time:
    """Parse HH:MM string into a datetime.time object."""
    hh_mm = RGX_HH_MM.match(input)
    if hh_mm is None:
        raise ValueError("Could not parse HH:MM from '{input}'")
    return datetime.time(*[int(digits) for digits in hh_mm.groups()])
