from typing import List, Tuple
import random
import matplotlib.pyplot as plt
import numpy as np
import warnings


from tsp_classes import City
import networkx as nx


def start_up(num_cities: int) -> Tuple[List[City], nx.Graph]:
    """
    Start up the assignment by creating cities on a canvas and storing them in a graph
    :param num_cities: THe number of cities
    :return: list of cities and a graph
    """
    MAX_X = 100
    MAX_Y = 100
    random.seed(1)

    cities = [City(id, random.randint(0, MAX_X), random.randint(0, MAX_Y)) for id in range(num_cities)]

    G = nx.DiGraph()
    for city in cities:
        G.add_node(city, pos=(city.location.x, city.location.y))

    return cities, G


def path_length(path: List[City]) -> float:
    """
    Calculate the total path length
    :param path: The path for which we calculate the length
    :return: path length
    """
    length = 0
    for index_from, city_from in enumerate(path):
        index_to = (index_from + 1) % len(path)
        city_to = path[index_to]
        length += city_from.distance_to(city_to)
    return length


def draw_path(G, path: List[City]):
    """
    Draw the path on the screen
    :param G: The graph with all cities
    :param path: The path that we want to draw
    :return: Figure with the path
    """
    G.remove_edges_from(list(G.edges.keys()))
    for index_from, city_from in enumerate(path):
        index_to = (index_from + 1) % len(path)
        city_to = path[index_to]
        G.add_edge(city_from, city_to)

    nx.draw(G, nx.get_node_attributes(G, 'pos'), node_size=5, with_labels=True)
    length = path_length(path)
    plt.title(f'Your provided solution with length {length}')
    plt.show()


def evaluate_path(path: List[City], cities: List[City], length_path: float):
    """
    Evaluate if a path is valid, all cities should be valid and the length should match
    :param path: The path to evaluate
    :param cities: All cities that need to be visited
    :param length_path: The total path length that you calculated
    :return: Print in terminal if the path is valid
    """
    if all(city in cities for city in path) and len(path) == len(cities) and len(set(path)) == len(set(cities)):
        if length_path - 0.1 <= path_length(path) <= length_path + 0.1:
            print('Solution is valid')
        else:
            print('Your path is valid, but the objective value is incorrect')
    else:
        print('Your path is incorrect. Remember that each city should be visited once')


def re_insert_path_segment(segment: Tuple[int, int], insert_left_index: int, reverse: bool, path: List[City],
                           length: float) -> Tuple[List[City], float]:
    """
    Function to pick up a path segment from the path and insert it elsewhere on the remaining path
    :param segment: Tuple of the indices of the segment to remove
    :param insert_left_index: Insert the removed segment after this index in the new solution
    :param reverse: bool If we want to reverse the segment
    :param path: The original path
    :param length: The original path length
    :return: the new path, new path length

    Example:
    Segment = (4, 6)
    Insert_left_index = 3
    Reverse = True
    Path = [City 0, City 7, City 8, City 2, City 5, City 6, City 1, City 4, City 9, City 3]
    Length = 335

    Output = ([City 0, City 7, City 8, City 2, City 1, City 6, City 5, City 4, City 9, City 3], 302.75)
    """

    # Make the algorithm fool proof
    if segment[0] > segment[1]:
        warnings.warn("Warning......The second element of the segment is larger than the first, I reversed them")
        segment = (segment[1], segment[0])

    # Acquire the cities left and right of the segment
    left = path[(segment[0] - 1) % len(path)]
    right = path[(segment[1] + 1) % len(path)]
    # Calculate the path length after removing the segment by breaking 2 arcs and creating 1 new arc
    length_after_removal = length \
                           - left.distance_to(path[segment[0]]) \
                           - path[segment[1]].distance_to(right) \
                           + left.distance_to(right)
    # Remove the segment from the path
    path_after_removal = path[:segment[0]] + path[segment[1] + 1:]
    # Acquire the segment
    path_segment = path[segment[0]: segment[1] + 1]
    if reverse:
        # Reverse if needed
        path_segment.reverse()

    # Make the algorithm fool proof
    if insert_left_index >= len(path) - (segment[1] - segment[0] + 1) + 1:
        warnings.warn("Warning......The insert_left_index is larger than the remaining path after removal of the segment, I append the segment to the end")
        insert_left_index = len(path) - (segment[1] - segment[0] + 1)

    # Find the two indices from the path after removal where we insert our segment
    insert_right_index = (insert_left_index + 1) % len(path_after_removal)
    # Calculate the added length by removing the arc between the left and right insert and reconnecting the arc segment
    new_length = length_after_removal \
                 - path_after_removal[insert_left_index].distance_to(path_after_removal[insert_right_index]) \
                 + path_after_removal[insert_left_index].distance_to(path_segment[0]) \
                 + path_segment[-1].distance_to(path_after_removal[insert_right_index])
    new_path = path_after_removal[: insert_left_index + 1] + path_segment + path_after_removal[insert_right_index:]
    return new_path, new_length