from decimal import Decimal

import pytest

from wgups.distance_table import DistanceTable

HUB = "4001 South 700 East 84107"
WHEELER_HISTORIC_FARM = "6351 South 900 East 84121"
WEST_VALLEY_PROSECUTOR = "3575 W Valley Central Station bus Loop 84119"


@pytest.fixture
def distance_table():
    return DistanceTable()


def test_same_dest(distance_table):
    assert distance_table.get_distance(HUB, HUB) == 0.0
    assert (
        distance_table.get_distance(WHEELER_HISTORIC_FARM, WHEELER_HISTORIC_FARM) == 0.0
    )
    assert (
        distance_table.get_distance(WEST_VALLEY_PROSECUTOR, WEST_VALLEY_PROSECUTOR)
        == 0.0
    )


def test_reverse(distance_table):
    assert distance_table.get_distance(HUB, WHEELER_HISTORIC_FARM) == 3.6
    assert distance_table.get_distance(WHEELER_HISTORIC_FARM, HUB) == 3.6


def test_long(distance_table):
    assert (
        distance_table.get_distance(WEST_VALLEY_PROSECUTOR, WHEELER_HISTORIC_FARM)
        == 13.6
    )
