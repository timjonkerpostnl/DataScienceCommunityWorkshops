import tsp_general_functions
import assignment1
import assignment2
import tsp_aco

NUM_CITIES = 10
cities, G = tsp_general_functions.start_up(NUM_CITIES)

# If you need to, you could make changes here, do not update the output variable names
# path, length, comp_time = assignment1.initial_solution(cities)
path, length, comp_time = assignment2.local_search(cities, grasp_iterations=20, fraction_of_best=1.2)
# path, length, comp_time = tsp_aco.aco(cities, num_ants=5, alpha=1, beta=2, rho=0.1,
#                                       q=10000, iterations=50, initial_pheromone_level=1, apply_2_opt=False)

# vvvvvv DON'T TOUCH THESE LINES IF YOU WANT TO FOLLOW THE ASSIGNMENT vvvvvvvv
tsp_general_functions.evaluate_path(path, cities, length)
print(f'Your solution has an objective value of {length} and was found in {comp_time} seconds')
tsp_general_functions.draw_path(G, path)
# ^^^^^^ DON'T TOUCH THESE LINES IF YOU WANT TO FOLLOW THE ASSIGNMENT ^^^^^^^^
