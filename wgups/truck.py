from typing import Set


class Truck:
    def __init__(self, id: int):
        self.id = id
        self.driver: int = None
        self.packages: Set[str] = set()
