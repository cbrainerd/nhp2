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
        self.constraint = constraint

        self.delivery_time: datetime.time = None
        self.delivery_truck: datetime.time = None

    def get_address(self):
        return f"{self.address} {self.zip}"

    def mark_delivered(self, delivery_time, delivery_truck):
        self.delivery_time = delivery_time
        self.delivery_truck = delivery_truck
        if delivery_time > self.deadline:
            print(f"Package {self.id} was LATE! Due at {self.deadline} delivered at {delivery_time}")

    def earliest_load(self):
        if not self.constraint or self.constraint.earliest_pickup is None:
            return datetime.time(0, 0)
        else:
            return self.constraint.earliest_pickup
