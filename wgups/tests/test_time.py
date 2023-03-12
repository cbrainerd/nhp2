import datetime

import pytest

from wgups.time import parse_time


def test_parse_time():
    assert parse_time("23:59") == datetime.time(23, 59)


def test_unparsable_time():
    """String that fails regex raises ValueError."""
    with pytest.raises(ValueError):
        parse_time("30:00")


def test_invalid_time():
    """String that passes regex but fails in datetime.time raises ValueError."""
    with pytest.raises(ValueError):
        parse_time("25:00")
