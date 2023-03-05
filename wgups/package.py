from datetime import time

from wgups.constraint import Constraint

class Package:
    def __init__(
        self,
        id: int,
        address: str,
        city: str,
        state: str,
        zip: str,  # String to allow zip+4
        delivery_deadline: time,
        mass: float,
        constraint: Constraint = None,
    ):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.delivery_deadline = delivery_deadline
        self.mass = mass
        self.constraint = constraint
