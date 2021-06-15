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
    path = cities
    total_distance = tsp_general_functions.path_length(path)
    # ^^^^^^ YOUR CODE HERE ^^^^^^^

    t_total = time.time() - t0

    return path, total_distance, t_total
