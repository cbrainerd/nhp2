from csv import reader
import os
import re

from wgups.hash_map import HashMap


# Parse addresses with format
#   Street Address (zip code)
RGX_ADDRESS = r"^\s*(.*) \(([0-9]+)\)\s*$"

class DistanceTable:

    def __init__(self, data_path=None):
        if data_path is None:
            data_path = os.path.join(os.path.dirname(__file__), "data", "distance_table.csv")

        # Set default as each value will be another HashMap. 
        self._distance_table = HashMap(default=HashMap)
        
        rgx_address = re.compile(RGX_ADDRESS)
        with open(data_path, "r", encoding="utf-8") as csv_file:
            data = reader(csv_file)
            addresses = list()
            for row in data:
                start_address = " ".join(rgx_address.match(row.pop(0)).groups())
                addresses.append(start_address)
                for address in addresses:
                    # Store distance for each address we've already seen. 
                    self._distance_table[start_address][address] = float(row.pop(0))
                    print(f"{start_address} to {address} is {self._distance_table[start_address][address]}")

        # Table loading is done, don't create any more default entries.           
        self._distance_table.set_default(None)
                
    def get_distance(self, origin: str, destination: str) -> float:
        if origin not in self._distance_table:
            raise ValueError(f"origin {origin} not found")
        if destination not in self._distance_table:
            raise ValueError(f"destination {destination} not found")
        try:
            distance = self._distance_table[destination][origin]
        except KeyError:
            # Distances are symmetrical, try the other direction
            distance = self._distance_table[origin][destination]
        return distance
    