from tsp_classes import City
from typing import List, Tuple
import numpy as np
import random
import time
import tsp_general_functions
import tsp_local_search
from numpy.random import choice
from operator import attrgetter

np.random.seed(1)


class Ant:
    """
    An ant is used as a metaphor for a solution. Therefore, it has a path and an associated path length
    Furthermore, it stores a list of all edges within the path
    """

    def __init__(self, city1: City, num_cities: int):
        self.path = [city1]
        self.path_length = 0
        self.used_edges = []
        self.num_cities = num_cities

    def add_to_path(self, city: City):
        """
        Add a city to the path. Update used edges. Update total distance
        :param city: City to append to the end of the path
        """
        if city in self.path:
            raise ValueError('THis city is already in the path')
        self.path_length += self.path[-1].distance_to(city)
        self.used_edges.append((self.path[-1], city))
        self.path.append(city)

        if len(self.path) == self.num_cities:
            # If it is the final city complete the tour by returning to the first city
            self.path_length += self.path[-1].distance_to(self.path[0])
            self.used_edges.append((self.path[-1], self.path[0]))

    def apply_2_opt(self):
        """
        Apply 2-opt to improve the Ants path
        :return:
        """
        self.path, self.path_length = tsp_local_search.two_opt(self.path)
        # put the city0 in front
        index_of_city0 = self.path.index(next(x for x in self.path if x.id == 0))
        self.path = self.path[index_of_city0:] + self.path[:index_of_city0]
        self.used_edges = []
        for index1, city1 in enumerate(self.path):
            index2 = (index1 + 1) % len(self.path)
            city2 = self.path[index2]
            self.used_edges.append((city1, city2))

    def reset_ant(self):
        """
        Reset the ant to its initial state
        :return:
        """
        self.path = [self.path[0]]
        self.path_length = 0
        self.used_edges = []


def aco(cities: List[City], num_ants=10, alpha=0.5, beta=1, rho=0.9, q=100, iterations=20, initial_pheromone_level=1,
        apply_2_opt: bool = False) -> Tuple[List[City], float, float]:
    """
    Apply Ant Colony Optimization
    :param cities: The cities to be visited
    :param num_ants: number of ants
    :param alpha: factor of the pheromone levels in the score function
    :param beta: factor of the distance in the score function
    :param rho: evaporation rate of pheromone levels
    :param q: factor to update the pheromone levels according to solution quality of ants
    :param iterations: the total number of iterations
    :param initial_pheromone_level: the initial pheromone level for every arc
    :param apply_2_opt: If True apply local search for each ant solution
    :return: The path, the objective, the computation time
    """
    # Create the ants
    ants = [Ant(cities[0], len(cities)) for _ in range(num_ants)]

    t0 = time.time()

    # Initialize pheromone levels
    pheromone_levels = {}
    for city1 in cities:
        pheromone_levels[city1] = {}
        for city2 in cities:
            pheromone_levels[city1][city2] = initial_pheromone_level

    best_solution = None
    best_objective = np.inf

    # During each iteration each ant builds a path
    for _ in range(iterations):
        # build paths
        for ant in ants:
            # Reset everything for this ant
            ant.reset_ant()
            unvisited_cities = set(cities[1:])
            while len(unvisited_cities) > 0:
                # Continue until all cities are visited
                scores = {}
                for city in unvisited_cities:
                    # For each city calculate the score
                    scores[city] = (pheromone_levels[ant.path[-1]][city] ** alpha) / \
                                   ((ant.path[-1].distance_to(city)) ** beta + 0.1)
                # Obtain the total score
                total_score = sum(score for score in scores.values())
                # Assign probabilities for each city. Higher score -> higher probability
                probabilities = {city: score / total_score for city, score in scores.items()}

                # Pick one city randomly while respecting the probabilities
                chosen_city = choice(list(probabilities.keys()), 1, p=list(probabilities.values()))[0]

                # Add the city to the path
                ant.add_to_path(chosen_city)
                unvisited_cities.remove(chosen_city)

            if apply_2_opt:
                ant.apply_2_opt()

        best_ant = min(ants, key=attrgetter('path_length'))
        # Update pheromone levels of all cities
        for city1 in cities:
            for city2 in cities:
                # pheromone_levels[city1][city2] = (1 - rho) * pheromone_levels[city1][city2] + \
                #                                  sum(q / ant.path_length for ant in ants if
                #                                      (city1, city2) in ant.used_edges)
                if (city1, city2) in best_ant.used_edges:
                    pheromone_levels[city1][city2] = (1 - rho) * pheromone_levels[city1][city2] + \
                                                     sum(q / ant.path_length for ant in ants if
                                                         (city1, city2) in ant.used_edges)
                else:
                    pheromone_levels[city1][city2] = (1 - rho) * pheromone_levels[city1][city2]

        # Remember the best solution

        if best_ant.path_length < best_objective:
            best_objective = best_ant.path_length
            best_solution = best_ant.path

    t_total = time.time() - t0

    return best_solution, best_objective, t_total
