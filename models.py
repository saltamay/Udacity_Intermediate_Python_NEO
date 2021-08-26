"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

"""
from typing import List
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(
            self,
            pdes: str,
            name: str = None,
            diameter: float = float('nan'),
            hazardous: bool = False,
            **info):
        """Create a new `NearEarthObject`.

        Arguments:
            pdes {str} -- The primary designation for this NEO.
            name {str} --  The IAU name for this NEO.
            diameter {float} -- The diameter, in kilometers, of this NEO
            hazardous {bool} -- Whether or not this NEO is potentially hazardous.
            **info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = pdes
        self.name = name
        self.diameter = diameter
        self.hazardous = hazardous

        # Create an empty initial collection of linked approaches.
        self.approaches: List[CloseApproach] = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f"{self.designation} ({self.name})"

    def __str__(self):
        """Return `str(self)`."""
        return (
            f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km and "
            f"{'is' if self.hazardous else 'is not'} potentially hazardous.")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
            f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(
            self,
            pdes: str,
            time: str,
            distance: float = float('nan'),
            velocity: float = float('nan'),
            neo: NearEarthObject = None,
            **info):
        f"""Create a new `CloseApproach`.

        Arguments:
            pdes {str} -- The primary designation for this NearEarthObject.
            time {str} -- The date and time, in UTC, at which the NEO passes closest to Earth.
            distance {float} -- The nominal approach distance of the NEO to Earth at the closest point.
            velocity {bool} -- The velocity, in km/sec, of the NEO relative to Earth at the closest point.
            neo {NearEarthObject} -- The NEO that is making a close approach to Earth.
            **info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = pdes
        self.time = cd_to_datetime(time)
        self.distance = distance
        self.velocity = velocity

        # Create an attribute for the referenced NEO, originally None.
        self.neo: NearEarthObject = neo

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return (
            f"On {self.time_str}, '{self.neo.fullname}' approaches Earth "
            f"at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s.")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
            f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    @property
    def designation(self):
        return self._designation
