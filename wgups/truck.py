from typing import List

class Truck:
    def __init__(self, id: int):
        self.id = id
        self.driver: int = None
        self.route: List[str] = None
