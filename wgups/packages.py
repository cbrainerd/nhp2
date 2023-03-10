from csv import reader
import datetime
import os
import time
from typing import List

from wgups.hash_table import HashTable
from wgups.constraint import Constraint
from wgups.logging import LOGGER
from wgups.package import Package
from wgups.time import EOD

# Truck designated to handle grouped packages
# (package x must be delivered with package y)
GROUPED_PACKAGE_TRUCK = 1


class Packages:
    def __init__(self, data_path: str = None):
        if data_path is None:
            data_path = os.path.join(
                os.path.dirname(__file__), "data", "package_table.csv"
            )

        # Load the packages hash table from the CSV data file.
        with open(data_path, "r", encoding="utf-8") as csv_file:
            data = reader(csv_file)
            self._packages = HashTable()
            for package in data:
                id = int(package.pop(0))
                address = package.pop(0)
                city = package.pop(0)
                state = package.pop(0)
                zip = package.pop(0)
                raw_deadline = package.pop(0)
                mass = int(package.pop(0))
                constraint_description = package.pop(0)

                if raw_deadline == "EOD":
                    deadline = EOD
                else:
                    deadline = time.strptime(raw_deadline, "%H:%M %p")
                    deadline = datetime.time(deadline.tm_hour, deadline.tm_min)

                # Parse any special instructions into a constraint.
                if constraint_description:
                    constraint = Constraint(from_description=constraint_description)
                else:
                    constraint = None

                self._packages[id] = Package(
                    id, address, city, state, zip, deadline, mass, constraint
                )
        # Ensure all grouped packages are loaded in the same truck.
        for package_id in self._packages.keys():
            if self._packages[package_id].with_packages is not None:
                self._packages[
                    package_id
                ].constraint.assigned_truck = GROUPED_PACKAGE_TRUCK
                for with_package_id in self._packages[package_id].with_packages:
                    self._packages[
                        with_package_id
                    ].constraint.assigned_truck = GROUPED_PACKAGE_TRUCK

    def get(self, id: int) -> Package:
        return self.__getitem__(id)

    def __getitem__(self, id: int) -> Package:
        return self._packages[id]

    def items(self) -> List[Package]:
        """Returns all packages."""
        return self._packages.items()

    def sorted_items(self) -> List[Package]:
        return sorted(self._packages.items(), key=lambda x: x.id)

    def ready_to_load(self, current_time: datetime.time) -> List[Package]:
        """Packages that are ready for pick up the current time and not already loaded on a truck."""
        ready = list()
        for package in self.items():
            if package.delivery_truck is not None:
                continue
            if current_time < package.earliest_load:
                continue
            ready.append(package)
        return ready

    def packages_in_hub(self) -> List[Package]:
        """Returns all packages in the hub."""
        in_hub = list()
        for package in self.items():
            if package.delivery_truck is None:
                in_hub.append(package)
        return in_hub

    def latest_load(self) -> datetime.time:
        """Returns the latest pickup time for packages not yet loaded on a truck"""
        latest_load = datetime.time(0, 0)
        for package in self.items():
            if package.delivery_truck is None and package.earliest_load > latest_load:
                latest_load = package.earliest_load
        return latest_load

    def print_at_time(self, time: datetime.time):
        print(f"\nPackage status report for {time}")
        print("----------------------------------")
        for package in self.sorted_items():
            print(f"id: {package.id:2} - status: {package.status(time)}")
