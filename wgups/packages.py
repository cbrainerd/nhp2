from csv import reader
import datetime
import os
import time

from wgups.hash_map import HashMap
from wgups.constraint import Constraint
from wgups.package import Package

GROUPED_PACKAGE_TRUCK = 1


class Packages:
    def __init__(self, data_path=None):
        if data_path is None:
            data_path = os.path.join(
                os.path.dirname(__file__), "data", "package_table.csv"
            )

        with open(data_path, "r", encoding="utf-8") as csv_file:
            data = reader(csv_file)
            self._packages = HashMap()
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
                    deadline = datetime.time(23, 59)
                else:
                    deadline = time.strptime(raw_deadline, "%H:%M %p")
                    deadline = datetime.time(deadline.tm_hour, deadline.tm_min)

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
                self._packages[package_id].constraint.assigned_truck = GROUPED_PACKAGE_TRUCK
                for with_package_id in self._packages[package_id].with_packages:
                    self._packages[with_package_id].constraint.assigned_truck = GROUPED_PACKAGE_TRUCK
                

    def get(self, id):
        return self.__getitem__(id)

    def __getitem__(self, id):
        return self._packages[id]

    def items(self):
        return self._packages.items()
    
    def ready_to_load(self, current_time):
        """Packages that are ready for pick up the current time and not already loaded on a truck"""
        ready = list()
        for package in self.items():
            if package.delivery_truck is not None:
                continue
            if current_time < package.earliest_load:
                continue
            ready.append(package)
        return ready
