from enum import Enum


class Node:
    def __init__(self, number, x, y):
        self.number = number
        self.x = x
        self.y = y


class NodeWithNeighbors(Node):
    def __init__(self, number, x, y, neighbors):
        self.neighbors = neighbors
        Node.__init__(self, number, x, y)


class DngResult:
    def __init__(self, best_route, cost, sub_tours, cardinality, start_delta1, final_delta1, delta2, exceeded,
                 elementary, iterations, time, ng_iterations):
        self.best_route = best_route
        self.cost = cost
        self.sub_tours = sub_tours
        self.cardinality = cardinality
        self.start_delta1 = start_delta1
        self.final_delta1 = final_delta1
        self.delta2 = delta2
        self.exceeded = exceeded
        self.elementary = elementary
        self.iterations = iterations
        self.time = time
        self.ng_iterations = ng_iterations


class NgResult:
    def __init__(self, best_route, cost, elementary, delta1, cardinality, time, ng_iterations):
        self.best_route = best_route
        self.cost = cost
        self.elementary = elementary
        self.delta1 = delta1
        self.cardinality = cardinality
        self.time = time
        self.ng_iterations = ng_iterations


class SortOption(Enum):
    delta2 = 1
    start_delta1 = 2
    final_delta1 = 3
    elementary = 4
    exceeded = 5
    iterations = 6
