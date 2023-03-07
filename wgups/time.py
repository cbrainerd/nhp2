import datetime


def add_time(start_time, time_delta) -> datetime.time:
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
