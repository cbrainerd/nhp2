import datetime

from wgups.constraint import Constraint
from wgups.time import EOD


class Package:
    def __init__(
        self,
        id: int,
        address: str,
        city: str,
        state: str,
        zip: str,  # String to allow zip+4
        deadline: datetime.time,
        mass: float,
        constraint: Constraint = None,
    ):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass

        if constraint is None:
            constraint = Constraint()
        self.constraint = constraint

        self.delivery_time: datetime.time = None
        self.delivery_truck: datetime.time = None
        self.time_loaded: datetime.time = None

    def get_address(self):
        """Return package address in "address zip" format."""
        return f"{self.address} {self.zip}"

    def mark_delivered(self, delivery_time, delivery_truck):
        """Called when package has been delivered to destination."""
        self.delivery_time = delivery_time
        self.delivery_truck = delivery_truck

    @property
    def earliest_load(self):
        """Earliest time that a package can be loaded at HUB."""
        if not self.constraint or self.constraint.earliest_pickup is None:
            return datetime.time(0, 0)
        else:
            return self.constraint.earliest_pickup

    @property
    def assigned_truck(self):
        """Indicates truck ID that must carry this package."""
        if not self.constraint or self.constraint.assigned_truck is None:
            return None
        else:
            return self.constraint.assigned_truck

    @property
    def with_packages(self):
        """Packages that must be delivered by the same truck."""
        if not self.constraint or self.constraint.with_packages is None:
            return None
        else:
            return self.constraint.with_packages

    def __str__(self):
        if self.delivery_time is not None:
            status = f"delivered by truck {self.delivery_truck} at {self.delivery_time}"
            if self.delivery_time > self.deadline:
                status += " *LATE*"
        elif self.delivery_time is None and self.delivery_truck is not None:
            status = f"enroute on truck {self.delivery_truck} loaded at {self.time_loaded} for delivery by {self.deadline}"
        elif self.delivery_truck is None:
            status = f"at HUB"
        return f"{self.id} - {status} - due at {self.deadline}"

    def __repr__(self):
        return self.__str__()

    def status(self, current_time: datetime.time):
        """Returns a human readable description of the package status."""
        if current_time >= self.delivery_time:
            late = " *LATE*" if self.delivery_time > self.deadline else ""
            status = f"DELIVERED by truck {self.delivery_truck} at {self.delivery_time}{late}"
        elif current_time >= self.time_loaded:
            deadline = "EOD" if self.deadline == EOD else self.deadline
            status = f"ENROUTE on truck {self.delivery_truck} loaded at {self.time_loaded} for delivery by {deadline}"
        elif current_time >= self.earliest_load:
            status = f"AT HUB - available for loading"
        else:
            status = f"AT HUB - available for loading at {self.earliest_load}"
        return status
