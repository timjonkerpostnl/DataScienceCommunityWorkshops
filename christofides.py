from typing import List, Tuple, Dict, Set
from tsp_classes import City
import time
import tsp_general_functions


def tsp(data) -> Tuple[List[City], float, float]:
    """
    This function subsequently builds a Christofides cycle,
    afterwards it improves the Christofides cycle with heuristics
    :param data: Set of Citys
    :return: List of Citys
    """
    # build a graph
    G = build_graph(data)

    t0 = time.time()

    # build a minimum spanning tree
    MSTree = minimum_spanning_tree(G)

    # find odd vertexes
    odd_vertexes = find_odd_vertexes(MSTree)

    # add minimum weight matching edges to MST
    minimum_weight_matching(MSTree, odd_vertexes)

    # find an eulerian tour
    eulerian_tour = find_eulerian_tour(MSTree)
    path = list(dict.fromkeys(eulerian_tour))

    length_christofides = tsp_general_functions.path_length(path)

    t_total = time.time() - t0

    return path, length_christofides, t_total


def build_graph(data) -> Dict[City, Dict[City, float]]:
    """
    :param data: All nodes in the graph
    :return: Dict of origin->desitination: distance
    """
    graph = {}
    for this in data:
        for another_point in data:
            if this != another_point:
                if this not in graph:
                    graph[this] = {}
                graph[this][another_point] = this.distance_to(another_point)
    return graph


class UnionFind:
    def __init__(self):
        self.weights = {}
        self.parents = {}

    def __getitem__(self, object):
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object

        # find path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]

        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root

    def __iter__(self):
        return iter(self.parents)

    def union(self, *objects):
        roots = [self[x] for x in objects]
        heaviest = max([(self.weights[r], r) for r in roots])[1]
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest


def minimum_spanning_tree(G):
    """
    Construct a minimum spanning tree
    :param G:
    :return:
    """
    tree = []
    subtrees = UnionFind()
    for W, u, v in sorted((G[u][v], u, v) for u in G for v in G[u]):
        if subtrees[u] != subtrees[v]:
            tree.append((u, v, W))
            subtrees.union(u, v)

    return tree


def find_odd_vertexes(MST):
    """
    Find the odd vertices in the MST
    :param MST:
    :return:
    """
    tmp_g = {}
    vertexes = []
    for edge in MST:
        if edge[0] not in tmp_g:
            tmp_g[edge[0]] = 0

        if edge[1] not in tmp_g:
            tmp_g[edge[1]] = 0

        tmp_g[edge[0]] += 1
        tmp_g[edge[1]] += 1

    for vertex in tmp_g:
        if tmp_g[vertex] % 2 == 1:
            vertexes.append(vertex)

    return vertexes


def minimum_weight_matching(MST, odd_vert: List[City]):
    """
    Conncet the odd vertices in an optimal way and add this to the MST
    :param MST:
    :param odd_vert:
    :return:
    """
    import random
    random.shuffle(odd_vert)

    while odd_vert:
        v = odd_vert.pop()
        length = float("inf")
        closest = 0
        for u in odd_vert:
            dist = v.distance_to(u)
            if v != u and dist < length:
                length = dist
                closest = u

        MST.append((v, closest, length))
        odd_vert.remove(closest)


def find_eulerian_tour(MatchedMSTree):
    """
    From the MatchedMSTree make eulerian tour by skipping visited nodes
    :param MatchedMSTree:
    :return:
    """
    # find neigbours
    neighbours = {}
    for edge in MatchedMSTree:
        if edge[0] not in neighbours:
            neighbours[edge[0]] = []

        if edge[1] not in neighbours:
            neighbours[edge[1]] = []

        neighbours[edge[0]].append(edge[1])
        neighbours[edge[1]].append(edge[0])

    # print("Neighbours: ", neighbours)

    # finds the hamiltonian circuit
    start_vertex = MatchedMSTree[0][0]
    EP = [neighbours[start_vertex][0]]

    while len(MatchedMSTree) > 0:
        for i, v in enumerate(EP):
            if len(neighbours[v]) > 0:
                break

        while len(neighbours[v]) > 0:
            w = neighbours[v][0]

            remove_edge_from_matchedMST(MatchedMSTree, v, w)

            del neighbours[v][(neighbours[v].index(w))]
            del neighbours[w][(neighbours[w].index(v))]

            i += 1
            EP.insert(i, w)

            v = w

    return EP


def remove_edge_from_matchedMST(MatchedMST, v1, v2):
    for i, item in enumerate(MatchedMST):
        if (item[0] == v2 and item[1] == v1) or (item[0] == v1 and item[1] == v2):
            del MatchedMST[i]

    return MatchedMST