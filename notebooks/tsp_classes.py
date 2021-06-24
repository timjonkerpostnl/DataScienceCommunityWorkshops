from typing import Tuple, Set, List, Dict
import numpy as np


class Location:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance(self, other) -> float:
        return np.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __str__(self):
        return "Loc x: {}, y: {}".format(self.x, self.y)

    def __repr__(self):
        return "Loc x: {}, y: {}".format(self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.x != other.x or self.y != other.y


class City:
    def __init__(self, id: int, x: float, y: float):
        self.id = id
        self.location = Location(x, y)

    def distance_to(self, other) -> float:
        """
        Calculate the distance to the other city
        :param other: Another city
        :return: euclidean distance between the two cities
        """
        return self.location.distance(other.location)

    def closest_other_city(self, other_cities):
        """
        Find the closest city among a list of other cities
        :param other_cities: List of cities from which we select the closest city
        :return: The closest city and minimal distance
        """
        best_extra_distance = np.inf
        best_city = None
        for city in other_cities:
            extra_distance = self.distance_to(city)
            if extra_distance < best_extra_distance:
                best_extra_distance = extra_distance
                best_city = city
        return best_city, best_extra_distance

    def closest_other_city_dict(self, other_cities):
        """
        Calculate the distance to each other city and store results in a dictionary.
        Also return the distance to the closest other city
        :param other_cities: Set of cities to which e calculate the distance
        :return: The closest city and minimal distance
        """
        best_extra_distance = np.inf
        extra_distances = {}
        # For each city calculate the distance
        for city in other_cities:
            extra_distances[city] = self.distance_to(city)
            if extra_distances[city] < best_extra_distance:
                # Remember the distance to the closest city
                best_extra_distance = extra_distances[city]
        return extra_distances, best_extra_distance

    def best_insertion_position(self, path) -> Tuple[int, float]:
        """
        Find the best position to insert self into a path of other cities
        :param path: THe path where we insert self
        :return: the index of the best insertion position (place self on this index)
        and the additional distance of the insertion
        """
        best_index = None
        best_extra_distance = np.inf
        for index1, city1 in enumerate(path):
            # For each position between city 1 and 2 calculate the insertion cost
            index2 = (index1 + 1) % len(path)
            city2 = path[index2]
            extra_distance = city1.distance_to(self) + self.distance_to(city2)
            if extra_distance < best_extra_distance:
                # Remember the best option
                best_extra_distance = extra_distance
                best_index = index2

        return best_index, best_extra_distance

    def __str__(self):
        return "City {}".format(self.id)

    def __repr__(self):
        return "City {}".format(self.id)

    def __hash__(self):
        return hash((self.id, self.location))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.id == other.id and self.location == other.location

    def __ne__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.id != other.id or self.location != other.location

    def __le__(self, other):
        return self.id <= other.id

    def __lt__(self, other):
        return self.id < other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __gt__(self, other):
        return self.id > other.id