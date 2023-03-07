# Chris Brainerd / Student ID: 010438858

import datetime
from typing import List

from wgups.distance_table import DistanceTable
from wgups.package import Package
from wgups.packages import Packages
from wgups.time import add_time
from wgups.truck import Truck, TruckFullException


HUB = "4001 South 700 East 84107"
NUM_TRUCKS = 2
RUSH_THRESHOLD = 30


class Scheduler:
    def __init__(self):
        self.distance_table = DistanceTable()
        self.packages = Packages()
        self.trucks = [
            Truck(id, HUB, datetime.time(8, 0)) for id in range(1, NUM_TRUCKS + 1)
        ]
        self.trucks[1].current_time = datetime.time(8, 0)

    def load_packages(self, truck):
        print(f"Loading truck {truck.id} at {truck.current_time}")
        try:
            for package in self.packages.ready_to_load(truck.current_time):
                if package.deadline < datetime.time(10, 30):
                    truck.load_package(package, truck.current_time)

            for package in self.packages.ready_to_load(truck.current_time):
                if package.deadline < datetime.time(23, 59):
                    if package.assigned_truck is not None:
                        if package.assigned_truck == truck.id:
                            truck.load_package(package, truck.current_time)
                        else:
                            continue
                    else:
                        truck.load_package(package, truck.current_time)

            for package in self.packages.ready_to_load(truck.current_time):
                if package.assigned_truck == truck.id:
                    truck.load_package(package, truck.current_time)
                else:
                    truck.load_package(package, truck.current_time)

        except TruckFullException:
            print(f"Truck {truck.id} is fully loaded.")

    def choose_closest_package(self, origin, packages) -> Package:
        min_distance = 9999999
        closest_package = None
        for package in packages:
            distance = self.distance_table.get_distance(origin, package.get_address())
            if distance < min_distance:
                min_distance = distance
                closest_package = package
        return closest_package
    
    def choose_earliest_packages(self, packages) -> List[Package]:
        earliest_deadline = datetime.time(23, 59, 59)
        earliest_packages = list()
        for package in packages:
            if package.deadline < earliest_deadline:
                earliest_deadline = package.deadline
                earliest_packages = [package]
            elif package.deadline == earliest_deadline:
                earliest_packages.append(package)
        return earliest_packages

    def choose_next(self, origin, packages, current_time):
        earliest_packages = self.choose_earliest_packages(packages)
        if add_time(current_time, datetime.timedelta(minutes=RUSH_THRESHOLD)) > earliest_packages[0].deadline:
            print(f"  RUSH for deadline {earliest_packages[0].deadline} {earliest_packages}")
            candidate_packages = earliest_packages
        else:
            candidate_packages = packages
        closest_package = self.choose_closest_package(origin, candidate_packages)
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
                        package = self.choose_next(
                            truck.current_location, truck.packages, truck.current_time
                        )
                        truck.deliver_package(package)
                    # No more packages, return to HUB.
                    truck.drive_to(HUB)
        return

    def main(self):
        self.deliver_packages(self.trucks)

        self.packages.print_all()

        total_distance = sum([truck.distance_traveled for truck in self.trucks])
        print(f"Total distance traveled {total_distance} miles")


def main():
    Scheduler().main()


if __name__ == "__main__":
    main()
