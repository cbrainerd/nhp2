import datetime

from wgups.constraint import Constraint


def test_truck():
    constraint = Constraint(from_description="Can only be on truck 2")
    assert constraint.assign_truck == 2

def test_earliest_pickup():
    constraint = Constraint(from_description="Delayed on flight---will not arrive to depot until 9:05 am")
    assert constraint.earliest_pickup == datetime.time(9, 5)

def test_with_packages():
    constraint = Constraint(from_description="Must be delivered with 15, 19")
    assert constraint.with_packages == {15, 19}
