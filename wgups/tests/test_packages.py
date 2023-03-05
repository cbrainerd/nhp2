import datetime

import pytest

from wgups.packages import Packages


@pytest.fixture
def packages():
    return Packages()


def test_packages(packages):
    for i in range(1, 41):
        assert i in packages._packages


def test_package_22(packages):
    package = packages.get(22)
    assert package.id == 22
    assert package.address == "6351 South 900 East"
    assert package.city == "Murray"
    assert package.state == "UT"
    assert package.zip == "84121"
    assert package.deadline == datetime.time(23, 59)
    assert package.mass == 2
    assert package.constraint is None


def test_package_3_constraint(packages):
    package = packages.get(3)
    assert package.constraint.assign_truck == 2


def test_package_14_constraint(packages):
    package = packages.get(14)
    assert package.constraint.with_packages == {15, 19}
