import datetime
import re
from typing import Set


RGX_EARLIEST_PICKUP = re.compile(r"until [0-9]{1,2}:[0-9]{2} [aMpP][mM]")
RGX_TIME = re.compile(r"([0-9]{1,2}):([0-9]{2}) ([aMpP][mM])")


class Constraint:
    def __init__(
        self,
        assigned_truck: int = None,
        earliest_pickup: datetime.time = None,
        with_packages: Set[int] = None,
        from_description: str = None,
    ):
        if from_description is not None:
            if from_description.startswith("Can only be on truck"):
                assigned_truck = int(from_description.split(" ")[-1])
            elif RGX_EARLIEST_PICKUP.search(from_description):
                hour, minute, ampm = RGX_TIME.search(from_description).groups()
                hour = int(hour)
                minute = int(minute)
                if ampm == "pm" or ampm == "PM":
                    hour += 12
                earliest_pickup = datetime.time(hour, minute)
            elif "Must be delivered with " in from_description:
                # Get a string containing the comma separated ids.
                ids = from_description.partition("Must be delivered with ")[-1]
                # Convert the ids into integers.
                with_packages = set([int(id) for id in ids.split(",")])
            else:
                raise ValueError(f"Could not interpret '{from_description}'")

        self.assigned_truck = assigned_truck
        self.earliest_pickup = earliest_pickup
        self.with_packages = with_packages
