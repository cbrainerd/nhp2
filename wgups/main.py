# Chris Brainerd / Student ID: 010438858

import datetime

from wgups.distance_table import DistanceTable
from wgups.packages import Packages
from wgups.truck import Truck, TruckFullException

HUB = "4001 South 700 East 84107"
TRUCK_MPH = 18
NUM_TRUCKS = 2

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
        self.trucks = [Truck(id) for id in range(1, NUM_TRUCKS + 1)]

    def load_packages(self, truck, current_time):
        print(f"Loading truck {truck.id} at {current_time}")
        early_load = False
        try:
            for package in self.packages.ready_to_load(current_time):
                if package.deadline < datetime.time(10, 30):
                    truck.load_package(package, current_time)
                    early_load = True

            for package in self.packages.ready_to_load(current_time):
                if package.deadline < datetime.time(23, 59):
                    if hash(package.id) % NUM_TRUCKS + 1 == truck.id:
                        truck.load_package(package, current_time)
                        early_load = True

            if early_load:
                print("Early morning deliveries load, leaving depot")
                return
            
            for package in self.packages.ready_to_load(current_time):
                if hash(package.id) % NUM_TRUCKS + 1 == truck.id:
                    truck.load_package(package, current_time)
        
        except TruckFullException:
            print(f"Truck {truck.id} is fully loaded.")





    def deliver_packages(self, truck: Truck):
        distance_traveled = 0.0
        current_time = datetime.time(8, 0)
        current_location = HUB
        while True:
            self.load_packages(truck, current_time)
            if len(truck.packages) == 0:
                print(f"Nothing to deliver, it's quitting time for truck {truck.id}")
                break
            for package in truck.packages:
                # TODO: pick packages smartly instead of sequentially
                destination = package.get_address()
                distance = self.distance_table.get_distance(current_location, destination)
                arrival_time = get_arrival_time(distance, TRUCK_MPH, current_time)

                
                truck.deliver_package(package, arrival_time)

                current_time = arrival_time
                current_location = destination
                distance_traveled += distance
                print(
                    f"Truck {truck.id} delivered package {package.id} to {package.address} at {arrival_time} total distance {round(distance_traveled, 1)}"
                )
            truck.packages.clear()
            distance = self.distance_table.get_distance(current_location, HUB)
            arrival_time = get_arrival_time(distance, TRUCK_MPH, current_time)
            current_time = arrival_time
            current_location = HUB
            distance_traveled += distance
            print(
                f"Truck {truck.id} returned to HUB at {arrival_time} total distance {round(distance_traveled, 1)}"
            )
        return distance_traveled
        

    def main(self):
        total_distance = 0
        print("Truck 1 -----------------------------------------")
        total_distance += self.deliver_packages(self.trucks[0])
        print("Truck 2 -----------------------------------------")
        total_distance += self.deliver_packages(self.trucks[1])
        print(f"Total distance traveled {total_distance} miles")


def main():
    Scheduler().main()


if __name__ == "__main__":
    main()
