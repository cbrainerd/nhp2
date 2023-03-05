from typing import List

MAX_PACKAGES = 16


class TruckFullException(RuntimeError):
    pass

class Truck:
    def __init__(self, id: int):
        self.id = id
        self.driver: int = None
        self.packages: List[str] = list()

    def load_package(self, package):
        if len(self.packages) >= MAX_PACKAGES:
            raise TruckFullException
        
        self.packages.append(package)
        package.delivery_truck = self.id
        print(f"Loaded package {package.id} on truck {self.id}")

