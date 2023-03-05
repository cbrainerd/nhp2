from csv import reader
import datetime
import os
import time

from wgups.hash_map import HashMap
from wgups.constraint import Constraint
from wgups.package import Package


class Packages:

    def __init__(self, data_path=None):
        if data_path is None:
            data_path = os.path.join(os.path.dirname(__file__), "data", "package_table.csv")


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

                self._packages[id] = Package(id, address, city, state, zip, deadline, mass, constraint)

    def get(self, id):
        return self.__getitem__(id)
    
    def __getitem__(self, id):
        return self._packages[id]
        