import random

import numpy as np
import pulp as plp
from Item import Item
from typing import List, Tuple
import time

random.seed(1)

CAPACITY = 1000
N_ITEMS = 100
MAX_VALUE = 100
MAX_WEIGHT = 100


def ilp(items: List[Item]) -> Tuple[int, float, List[Item]]:
    """
    Solve the knapsack problem with CMD COIN an ILP solution
    :param items: list of items
    :return: objective value, computational time, selected items
    """
    t0 = time.time()
    prob = plp.LpProblem("knapsack", plp.LpMaximize)
    select = plp.LpVariable.dicts("Use item", items, 0, 1, plp.LpBinary)
    # The objective function is added to 'prob' first
    prob += plp.lpSum([item.value * var for item, var in select.items()])
    prob += plp.lpSum([item.weight * var for item, var in select.items()]) <= CAPACITY, "Maximum capacity"
    solver = plp.PULP_CBC_CMD(msg=False)
    prob.solve(solver)
    t_total = time.time() - t0
    selected = [item for item, var in select.items() if var.varValue > 0.1]
    obj = prob.objective.value()
    return obj, t_total, selected


def dp(items: List[Item]) -> Tuple[int, float]:
    """
    Solve the knapsack problem with DP
    :param items: list of items
    :return: objective value, computational time
    """
    t0 = time.time()
    v = np.zeros((len(items), CAPACITY + 1))
    v[0, items[0].weight:] = items[0].value
    for count, item in enumerate(items[:-1]):
        for theta in range(0, CAPACITY + 1):
            idx = theta - items[count + 1].weight
            if idx < 0:
                value = -np.inf
            else:
                value = v[count, idx]

            v[count + 1, theta] = np.maximum(v[count, theta], value + items[count + 1].value)

    t_total = time.time() - t0

    objective = v[-1, -1]
    return objective, t_total


def approximation(items: List[Item]) -> Tuple[int, float]:
    """
    Solve the knapsack problem with Approximation
    :param items: list of items
    :return: objective value, computational time
    """
    t0 = time.time()
    weights = [item.weight for item in items]
    cum_weight = np.cumsum(weights)
    value_sum = sum(item.value for count, item in enumerate(items) if cum_weight[count] <= CAPACITY)
    value = np.maximum(value_sum, max(item.value for item in items))
    t_total = time.time() - t0

    return value, t_total


def greedy(items: List[Item]) -> Tuple[int, float, List[Item]]:
    """
    Solve the knapsack problem with Greedy constructive heuristic
    :param items: list of items
    :return: objective value, computational time
    """
    t0 = time.time()
    total_weight = 0
    selected_items = []
    for item in items:
        if item.weight + total_weight <= CAPACITY:
            selected_items.append(item)
            total_weight += item.weight

    t_total = time.time() - t0
    obj = sum(item.value for item in selected)
    return obj, t_total, selected


def grasp(items: List[Item]) -> Tuple[int, float, List[Item]]:
    """
    Solve the knapsack problem with GRASP
    :param items: list of items
    :return: objective value, computational time
    """
    t0 = time.time()
    total_weight = 0
    selected_items = []
    best_sol = []
    best_obj = 0
    for _ in range(20):
        for item in items:
            if item.weight + total_weight <= CAPACITY and random.random() <= 0.9:
                selected_items.append(item)
                total_weight += item.weight
        obj = sum(item.value for item in selected)
        if obj > best_obj:
            best_obj = obj
            best_sol = selected

    t_total = time.time() - t0
    return best_obj, t_total, best_sol


items = [Item(id, random.randint(1, MAX_VALUE), random.randint(1, MAX_WEIGHT)) for id in range(N_ITEMS)]
items.sort(reverse=True)

obj_ilp, t_total_ilp, selected = ilp(items)
obj_dp, t_total_dp, = dp(items)
obj_approx, t_total_approx, = approximation(items)
obj_greedy, t_total_greedy, selected_greedy = greedy(items)
obj_grasp, t_total_grasp, selected_grasp = grasp(items)


