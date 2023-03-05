from datetime import time
from typing import List


class Constraint:
    def __init__(
        self,
        assign_truck: int = None,
        earliest_pickup: time = None,
        with_packages: List[int] = None,
    ):
        self.assign_truck = assign_truck
        self.earliest_pickup = earliest_pickup
        self.with_packages = with_packages
