import tsp_general_functions
import assignment1
import assignment2

NUM_CITIES = 10
cities, G = tsp_general_functions.start_up(NUM_CITIES)

# If you need to, you could make changes here, do not update the output variable names
path, length, comp_time = assignment1.initial_solution(cities)
# path, length, comp_time = assignment2.local_search(cities, grasp_iterations=20, fraction_of_best=1.2)

# vvvvvv DON'T TOUCH THESE LINES IF YOU WANT TO FOLLOW THE ASSIGNMENT vvvvvvvv
tsp_general_functions.evaluate_path(path, cities, length)
print(f'Your solution has an objective value of {length} and was found in {comp_time} seconds')
tsp_general_functions.draw_path(G, path)
# ^^^^^^ DON'T TOUCH THESE LINES IF YOU WANT TO FOLLOW THE ASSIGNMENT ^^^^^^^^
