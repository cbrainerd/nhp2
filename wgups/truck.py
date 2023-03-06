from typing import List

MAX_PACKAGES = 16


class TruckFullException(RuntimeError):
    pass

class Truck:
    def __init__(self, id: int):
        self.id = id
        self.driver: int = None
        self.packages: List[str] = list()

    def load_package(self, package, current_time):
        if len(self.packages) >= MAX_PACKAGES:
            raise TruckFullException
        
        if current_time < package.earliest_load():
            raise RuntimeError(f"Violated earliest load {package.earliest_load()} for package {package.id}. ")
        
        self.packages.append(package)
        package.delivery_truck = self.id
        print(f"Loaded package {package.id} on truck {self.id}")

    def deliver_package(self, package, delivery_time):
        package.mark_delivered(delivery_time, self.id)