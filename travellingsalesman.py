import tsp_general_functions
import tsp_local_search
import tsp_aco

NUM_CITIES = 10
cities, G = tsp_general_functions.start_up(NUM_CITIES)


path_nearest_neighbour, length_nearest_neighbour, time_nearest_neighbour = tsp_local_search.greedy_nearest_neighbour(cities)
path_insertion, length_insertion, time_insertion = tsp_local_search.greedy_insertion_heuristic(cities)
path_grasp_nearest_neighbour, length_grasp_nearest_neighbour, time_grasp_nearest_neighbour = tsp_local_search.grasp_nearest_neighbour(cities, 200, 2.5)
path_local_search, length_local_search, time_local_search = tsp_local_search.local_search(cities)
path_aco, length_aco, time_aco = tsp_aco.aco(cities, num_ants=20, alpha=0.5, beta=1, rho=0.9,
                                 q=1000, iterations=20, initial_pheromone_level=1, apply_2_opt=False)

tsp_general_functions.evaluate_path(path_grasp_nearest_neighbour, cities, length_grasp_nearest_neighbour)
tsp_general_functions.draw_path(G, path_local_search)