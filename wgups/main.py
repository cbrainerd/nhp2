# Chris Brainerd / Student ID: 010438858

import datetime

from wgups.distance_table import DistanceTable
from wgups.packages import Packages
from wgups.truck import Truck

HUB = "4001 South 700 East 84107"
TRUCK_MPH = 18


def get_arrival_time(distance, velocity, start_time: datetime.time) -> datetime.time:
    duration = distance / velocity
    start_datetime = datetime.datetime(
        2000,
        1,
        1,
        start_time.hour,
        start_time.minute,
        start_time.second,
        start_time.microsecond,
    )
    end_datetime = start_datetime + datetime.timedelta(hours=duration)
    return end_datetime.time()


class Scheduler:
    def __init__(self):
        self.distance_table = DistanceTable()
        self.packages = Packages()
        self.trucks = [Truck(id) for id in range(1, 2)]

    def load_packages(self):
        self.trucks[0].packages = [self.packages[i] for i in range(1, 41)]

    def deliver_packages(self, truck: Truck):
        distance_travelled = 0.0
        current_time = datetime.time(8, 0)
        current_location = HUB
        for package in truck.packages:
            destination = package.get_address()
            distance = self.distance_table.get_distance(current_location, destination)
            arrival_time = get_arrival_time(distance, TRUCK_MPH, current_time)
            current_time = arrival_time
            current_location = destination
            distance_travelled += distance
            print(
                f"Truck delivered package ID {package.id} to {package.address} at {arrival_time} total distance {round(distance_travelled, 1)}"
            )

    def main(self):
        self.load_packages()
        self.deliver_packages(self.trucks[0])


def main():
    Scheduler().main()


if __name__ == "__main__":
    main()
