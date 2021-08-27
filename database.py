"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""
from typing import List
from models import NearEarthObject, CloseApproach
from filters import AttributeFilter


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(
            self,
            neos: List[NearEarthObject],
            approaches: List[CloseApproach]):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        Arguments:
            neos {List[NearEarthObject]}: A collection of `NearEarthObject`s.
            approaches {List[CloseApproach]}: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        self._data_map = {}

        # Link together the NEOs and their close approaches.
        for neo in self._neos:
            designation = neo.designation
            self._data_map[designation] = neo

        for approach in self._approaches:
            designation = approach.designation
            if self._data_map[designation]:
                approach.neo = self._data_map[designation]
                self._data_map[designation].approaches.append(approach)

    def get_neo_by_designation(self, designation: str) -> NearEarthObject:
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        Arguments:
            designation {str}: The primary designation of the NEO to search for.

        Return
            neo {NearEarthObject}: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        for neo in self._neos:
            if neo.designation == designation:
                return neo

        return None

    def get_neo_by_name(self, name: str) -> NearEarthObject:
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        Arguments:
            name {str}: The name, as a string, of the NEO to search for.

        Return:
            neo {NearEarthObject}: The `NearEarthObject` with the desired name, or `None`.
        """
        for neo in self._neos:
            if neo.name == name:
                return neo
        return None

    def query(self, filters: List[AttributeFilter]
              = ()) -> List[CloseApproach]:
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        Arguments:
            filters {List[AttributeFilter]}: A collection of filters capturing user-specified criteria.

        Return
            A stream of matching `CloseApproach` objects.
        """
        for approach in self._approaches:
            if self.filter(approach, filters):
                yield approach

    def filter(
            self,
            approach: CloseApproach,
            filters: List[AttributeFilter]) -> bool:
        """Apply filters.

        This return True or False depending if the approach passed all the filters

        Arguments:
            filters {List[AttributeFilter]}: A collection of filters capturing user-specified criteria.
            approach {CloseApproach}: A close approac
        Return
            True or False
        """
        for filter in filters:
            if filter(approach) is False:
                return False
        return True
