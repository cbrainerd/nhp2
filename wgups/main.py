# Chris Brainerd / Student ID: 010438858

import datetime
import math
from typing import List

from wgups.distance_table import DistanceTable
from wgups.logging import LOGGER
from wgups.package import Package
from wgups.packages import Packages, EOD
from wgups.time import add_time, parse_time
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

    def load_packages(self, truck: Truck):
        """Load a truck with packages from the hub."""
        LOGGER.debug(f"Loading truck {truck.id} at {truck.current_time}")
        if truck.current_location != HUB:
            raise RuntimeError("Attempt to load truck that isn't at HUB")
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

            if truck.current_time < self.packages.latest_load():
                # Don't load EOD packages until all packages with earlier deadlines are loaded.
                LOGGER.debug(f"Truck {truck.id} leaving behind EOD packages.")
                return

            # Tranche 3: load packages due at EOD
            for package in self.packages.ready_to_load(truck.current_time):
                if package.assigned_truck == truck.id:
                    truck.load_package(package, truck.current_time)
                else:
                    truck.load_package(package, truck.current_time)

        except TruckFullException:
            LOGGER.debug(f"Truck {truck.id} is fully loaded.")

    def choose_next(self, origin: str, packages: List[Package]) -> Package:
        """Chose the closest package to origin."""
        min_distance = math.inf
        closest_package = None
        # Iterate over packages and find the package closest to the origin.
        for package in packages:
            distance = self.distance_table.get_distance(origin, package.get_address())
            if distance < min_distance:
                min_distance = distance
                closest_package = package
        return closest_package

    def deliver_packages(self, trucks: List[Truck]):
        """Main load-delivery loop."""
        while True:
            for truck in trucks:
                while len(self.packages.packages_in_hub()) > 0:
                    self.load_packages(truck)
                    if len(truck.packages) != 0:
                        # Loading complete.
                        break
                    # Nothing loaded, no packages currently meet criteria to be loaded. Wait a few
                    # minutes and check again.
                    truck.current_time = add_time(
                        truck.current_time, datetime.timedelta(minutes=5)
                    )

            if sum(len(truck.packages) for truck in trucks) == 0:
                # No packages loaded on any truck, we're done.
                break

            for truck in trucks:
                while len(truck.packages):
                    package = self.choose_next(truck.current_location, truck.packages)
                    truck.deliver_package(package)
                # No more packages, return to HUB.
                truck.drive_to(HUB)
        return

    def total_distance(self):
        """Print the total distance traveled by all trucks."""
        distance = sum([truck.distance_traveled for truck in self.trucks])
        print(f"Trucks traveled a total distance of {distance} miles.")

    def main(self):
        # Execute the main delivery loop to determine trucks loads, routings,
        # delivery times, etc.
        self.deliver_packages(self.trucks)

        # Present the user interface.
        while True:
            print("\nWGUPS")
            print("---------------------------------------")
            print("(a) - all package info")
            print("(d) - distance traveled by all trucks")
            print("(t) - package status at time")
            print("(q) - quit")
            print("---------------------------------------")
            command = input("Choose an option: ")
            if command == "a":
                self.packages.print_at_time(EOD)
            elif command == "d":
                self.total_distance()
            elif command == "t":
                input_string = input("Enter time HH:MM: ")
                time = parse_time(input_string)
                self.packages.print_at_time(time)
            elif command == "q":
                break
            else:
                print("Invalid entry - try again")


def main():
    Scheduler().main()


if __name__ == "__main__":
    main()
