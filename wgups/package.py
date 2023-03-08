import datetime

from wgups.constraint import Constraint


class Package:
    def __init__(
        self,
        id: int,
        address: str,
        city: str,
        state: str,
        zip: str,  # String to allow zip+4
        deadline: datetime.time,
        mass: float,
        constraint: Constraint = None,
    ):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass

        if constraint is None:
            constraint = Constraint()
        self.constraint = constraint

        self.delivery_time: datetime.time = None
        self.delivery_truck: datetime.time = None

    def get_address(self):
        return f"{self.address} {self.zip}"

    def mark_delivered(self, delivery_time, delivery_truck):
        self.delivery_time = delivery_time
        self.delivery_truck = delivery_truck

    @property
    def earliest_load(self):
        if not self.constraint or self.constraint.earliest_pickup is None:
            return datetime.time(0, 0)
        else:
            return self.constraint.earliest_pickup

    @property
    def assigned_truck(self):
        if not self.constraint or self.constraint.assigned_truck is None:
            return None
        else:
            return self.constraint.assigned_truck

    @property
    def with_packages(self):
        if not self.constraint or self.constraint.with_packages is None:
            return None
        else:
            return self.constraint.with_packages

    def __str__(self):
        if self.delivery_time is not None:
            status = f"delivered by truck {self.delivery_truck} at {self.delivery_time}"
            if self.delivery_time > self.deadline:
                status += " *LATE*"
        elif self.delivery_time is None and self.delivery_truck is not None:
            status = f"enroute on truck {self.delivery_truck} for delivery by {self.deadline}"
        elif self.delivery_truck is None:
            status = f"at HUB"
        return f"{self.id} - {status}"

    def __repr__(self):
        return self.__str__()
