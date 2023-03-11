# Chris Brainerd / Student ID: 010438858

import datetime
import sys
from typing import List

from wgups.distance_table import DistanceTable
from wgups.logging import LOGGER
from wgups.package import Package
from wgups.packages import Packages
from wgups.truck import Truck, TruckFullException


HUB = "4001 South 700 East 84107"
NUM_TRUCKS = 2


class Scheduler:
    def __init__(self):
        self.distance_table = DistanceTable()
        self.packages = Packages()
        self.trucks = [
            Truck(id, HUB, datetime.time(8, 0)) for id in range(1, NUM_TRUCKS + 1)
        ]

    def load_packages(self, truck):
        LOGGER.debug(f"Loading truck {truck.id} at {truck.current_time}")
        try:
            # Tranche 1: load packages with earliest deadlines
            for package in self.packages.ready_to_load(truck.current_time):
                if package.deadline < datetime.time(10, 30):
                    truck.load_package(package, truck.current_time)

            # Tranche 2: load packages with deadlines
            for package in self.packages.ready_to_load(truck.current_time):
                if package.deadline < datetime.time(12, 0):
                    if package.assigned_truck is not None:
                        if package.assigned_truck == truck.id:
                            truck.load_package(package, truck.current_time)
                        else:
                            continue
                    else:
                        truck.load_package(package, truck.current_time)

            if len(truck.packages):
                return

            for package in self.packages.ready_to_load(truck.current_time):
                if package.assigned_truck == truck.id:
                    truck.load_package(package, truck.current_time)
                else:
                    truck.load_package(package, truck.current_time)

        except TruckFullException:
            LOGGER.debug(f"Truck {truck.id} is fully loaded.")

    def choose_closest_package(self, origin, packages) -> Package:
        min_distance = 9999999
        closest_package = None
        for package in packages:
            distance = self.distance_table.get_distance(origin, package.get_address())
            if distance < min_distance:
                min_distance = distance
                closest_package = package
        return closest_package

    def choose_next(self, origin, packages):
        closest_package = self.choose_closest_package(origin, packages)
        return closest_package

    def deliver_packages(self, trucks: List[Truck]):
        while True:
            for truck in trucks:
                self.load_packages(truck)

            if sum(len(truck.packages) for truck in trucks) == 0:
                # No packages loaded on trucks.
                break

            for truck in trucks:
                while len(truck.packages):
                    package = self.choose_next(truck.current_location, truck.packages)
                    truck.deliver_package(package)
                # No more packages, return to HUB.
                truck.drive_to(HUB)
        return

    def main(self):
        self.deliver_packages(self.trucks)

        self.packages.print_all()

        total_distance = sum([truck.distance_traveled for truck in self.trucks])
        LOGGER.debug(f"Total distance traveled {total_distance} miles")


def main():
    Scheduler().main()


if __name__ == "__main__":
    main()
