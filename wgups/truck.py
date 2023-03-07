import datetime
from typing import List

from wgups.distance_table import DistanceTable
from wgups.time import add_time

TRUCK_MPH = 18
MAX_PACKAGES = 16

DISTANCE_TABLE = DistanceTable()


def get_distance(origin: str, destination: str) -> float:
    return DISTANCE_TABLE.get_distance(origin, destination)


def get_arrival_time(distance, start_time: datetime.time) -> datetime.time:
    return add_time(start_time, datetime.timedelta(hours=distance / TRUCK_MPH))


class TruckFullException(RuntimeError):
    pass


class Truck:
    def __init__(self, id: int, current_location: str, current_time: datetime.time):
        self.id = id
        self.driver: int = None
        self.packages: List[str] = list()
        self.distance_traveled = 0
        self.current_location = current_location
        self.current_time = current_time
        self.distance_table = DistanceTable()

    def load_package(self, package, current_time):
        if len(self.packages) >= MAX_PACKAGES:
            raise TruckFullException

        if current_time < package.earliest_load:
            raise RuntimeError(
                f"Violated earliest load {package.earliest_load} for package {package.id}. "
            )

        assigned_truck = package.assigned_truck
        if assigned_truck is not None and assigned_truck != package.assigned_truck:
            raise RuntimeError(
                f"Violated assigned truck rule {package.assigned_truck} for package {package.id}"
            )

        self.packages.append(package)
        package.delivery_truck = self.id

    def drive_to(self, destination):
        distance = get_distance(self.current_location, destination)
        arrival_time = get_arrival_time(distance, self.current_time)
        self.current_location = destination
        self.distance_traveled += distance
        self.current_time = arrival_time
        print(
            f"Truck {self.id} drove to {destination} at {self.current_time} total distance {round(self.distance_traveled, 1)}"
        )

    def deliver_package(self, package):
        self.drive_to(package.get_address())
        package.mark_delivered(self.current_time, self.id)
        self.packages.remove(package)
        print(
            f"Truck {self.id} delivered package {package.id} at {self.current_time} "
            f"deadline was {package.deadline}"
        )
