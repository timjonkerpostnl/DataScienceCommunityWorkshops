from tsp_classes import City
from typing import List, Tuple
import numpy as np
import random
import time
import tsp_general_functions


def initial_solution(cities: List[City]) -> Tuple[List[City], float, float]:
    """
    Apply your constructive heuristic algorithm.
    :param cities: all cities to be visited
    :return: The path, the objective, the computation time
    """
    t0 = time.time()

    # vvvvvvv YOUR CODE HERE vvvvvvv
    # Hint: There are useful functions in the City class
    path = [cities[0]]
    unvisited_cities = set(cities[1:])
    while len(path) != len(cities):
        closest_city, distance = path[-1].closest_other_city(unvisited_cities)
        path.append(closest_city)
        unvisited_cities.remove(closest_city)

    # path = [cities[0]]
    # unvisited_cities = set(cities[1:])
    # while len(path) != len(cities):
    #     extra_dist = np.inf
    #     best_city = None
    #     best_index = None
    #     for city in unvisited_cities:
    #         insertion_position, extra_dist_insertion = city.best_insertion_position(path)
    #         if extra_dist_insertion < extra_dist:
    #             extra_dist = extra_dist_insertion
    #             best_city = city
    #             best_index = insertion_position
    #     path.insert(best_index, best_city)
    #     unvisited_cities.remove(best_city)

    total_distance = tsp_general_functions.path_length(path)
    # ^^^^^^ YOUR CODE HERE ^^^^^^^

    t_total = time.time() - t0

    return path, total_distance, t_total
