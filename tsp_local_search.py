from tsp_classes import City
from typing import List, Tuple
import numpy as np
import random
import time
import tsp_general_functions


def greedy_nearest_neighbour(cities: List[City]) -> Tuple[List[City], float, float]:
    """
    Apply the greedy nearest neighbour algorithm. Starting in city 0 visit the closest city as your next city
    :param cities: all cities to be visited
    :return: The path, the objective, the computation time
    """
    t0 = time.time()

    # Start in city 0
    path = [cities[0]]
    total_distance = 0
    unvisited_cities = set(cities[1:])
    while len(unvisited_cities) > 0:
        # Continue until all cities are visited
        # Find the city that if appended to the end gives the least additional distance
        best_city, best_extra_distance = path[-1].closest_other_city(unvisited_cities)
        # Add the best option to the path, and do the bookkeeping
        path.append(best_city)
        total_distance += best_extra_distance
        unvisited_cities.remove(best_city)

    # Complete the tour length by returning to the start position
    total_distance += path[-1].distance_to(path[0])
    t_total = time.time() - t0

    return path, total_distance, t_total


def greedy_insertion_heuristic(cities: List[City]) -> Tuple[List[City], float, float]:
    """
    Apply the greedy insertion heuristic. Insert the city at the position that increases the objective value the least
    :param cities: all cities to be visited
    :return: The path, the objective, the computation time
    """
    t0 = time.time()
    path = [cities[0]]
    unvisited_cities = set(cities[1:])
    while len(unvisited_cities) > 0:
        # Continue until all cities are visited
        best_extra_distance = np.inf
        best_city = None
        best_index = None
        for city in unvisited_cities:
            # Find the insertion cost for each unvisited city
            my_best_index, my_insertion_cost = city.best_insertion_position(path)
            if my_insertion_cost < best_extra_distance:
                # Remember the best option
                best_extra_distance = my_insertion_cost
                best_city = city
                best_index = my_best_index

        # Execute the best option and do the bookkeeping
        path.insert(best_index, best_city)
        unvisited_cities.remove(best_city)

    # Calculate the path length
    total_distance = tsp_general_functions.path_length(path)
    t_total = time.time() - t0

    return path, total_distance, t_total


def grasp_nearest_neighbour(cities: List[City], iterations=20, fraction_of_best=1.2):
    """
    Extend the nearest neighbour heuristic with GRASP. Select one city no further than fraction_of_best * d_closest city
    :param cities: all cities to be visited
    :param iterations: The number of GRASP iterations
    :param fraction_of_best: The fraction for which cities are accepted
    :return: The path, the objective, the computation time
    """
    t0 = time.time()
    best_path = None
    best_objective = np.inf
    for _ in range(iterations):
        # Repeat for all iterations
        path = [cities[0]]
        total_distance = 0
        unvisited_cities = set(cities[1:])
        while len(unvisited_cities) > 0:
            # Continue until all cities are visited
            # Find the extra distance to each unvisited city and the distance to the closest city
            extra_distances, best_extra_distance = path[-1].closest_other_city_dict(unvisited_cities)
            # Consider all cities that are within fraction_of_best * best_extra_distance distance
            options = [city for city, extra_distance in extra_distances.items()
                       if extra_distance <= fraction_of_best * best_extra_distance]
            # Select one of these cities randomly
            chosen_city = options[random.randint(0, len(options) - 1)]
            # Add this city to the path and do the bookkeeping
            path.append(chosen_city)
            total_distance += extra_distances[chosen_city]
            unvisited_cities.remove(chosen_city)

        # Calculate the path length by connecting the last and first city
        total_distance += path[-1].distance_to(path[0])
        if total_distance < best_objective:
            # If the obtained path is the best one so far remember it
            best_objective = total_distance
            best_path = path

    t_total = time.time() - t0

    return best_path, best_objective, t_total


def local_search(cities: List[City], grasp_iterations=20, fraction_of_best=1.2):
    """
    Apply local search to improve the solution obtained with GRASP
    :param cities: all cities to be visited
    :param grasp_iterations: The number of GRASP iterations
    :param fraction_of_best: The fraction for which cities are accepted
    :return: The path, the objective, the computation time
    """
    t0 = time.time()
    path, length, time_initial = grasp_nearest_neighbour(cities, grasp_iterations, fraction_of_best)
    path, length = two_opt(path)
    t_total = time.time() - t0
    return path, length, t_total


def two_opt(path: List[City]) -> Tuple[List[City], float]:
    """
    2-opt heuristic for path optimization. Destroy 2 arcs, reverse middle part and reconnect
    :param path: Original path (is updated in place)
    :return: The new path and the total length
    """
    improvement = True
    while improvement:
        improvement = False
        # Continue improving until there are no more improvements to be found
        for i in range(len(path) - 2):
            for k in range(i + 2, len(path)):
                if _cost_change_two_opt(path[i - 1], path[i], path[k - 1], path[k]) < -0.01:
                    path[i:k] = reversed(path[i:k])
                    improvement = True
    length = tsp_general_functions.path_length(path)
    return path, length


def _cost_change_two_opt(n1: City, n2: City, n3: City, n4: City):
    """
    0...n1-n2...n3-n4...N
    0...n1-n3...n2-n4...N
    :return: Cost gain of this change, at negative values it is an improvement
    """
    return n1.distance_to(n3) + n2.distance_to(n4) - n1.distance_to(n2) - n3.distance_to(n4)