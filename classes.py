from enum import Enum

# A class that holds all information of a node: its number and x and y coordinate
class Node:
    def __init__(self, number, x, y):
        self.number = number
        self.x = x
        self.y = y


# A class that inherits from Node and adds a list of neighbors of the Node
class NodeWithNeighbors(Node):
    def __init__(self, number, x, y, neighbors):
        self.neighbors = neighbors
        Node.__init__(self, number, x, y)


# A class that holds all information of a Dynamic Ng-Path Relaxation result
class DngResult:
    def __init__(self, best_route, cost, len_sub_tours, start_delta1, final_delta1, delta2, exceeded,
                 elementary, dng_iterations, time, all_ext, followed_ext, ub_ext, lut_ext, lut_up_ext, oob_ext, feasible_solutions):
        self.best_route = best_route
        self.cost = cost
        self.len_sub_tours = len_sub_tours
        self.start_delta1 = start_delta1
        self.final_delta1 = final_delta1
        self.delta2 = delta2
        self.exceeded = exceeded
        self.elementary = elementary
        self.dng_iterations = dng_iterations
        self.time = time
        self.all_ext = all_ext
        self.followed_ext = followed_ext
        self.ub_ext = ub_ext
        self.lut_ext = lut_ext
        self.lut_up_ext = lut_up_ext
        self.oob_ext = oob_ext
        self.feasible_solutions = feasible_solutions


# A class that holds all information of a Ng-Route Relaxation result
class NgResult:
    def __init__(self, best_route, cost, elementary, delta1, time, all_ext, followed_ext, ub_ext, lut_ext, lut_up_ext, oob_ext, feasible_solutions):
        self.best_route = best_route
        self.cost = cost
        self.elementary = elementary
        self.delta1 = delta1
        self.time = time
        self.all_ext = all_ext
        self.followed_ext = followed_ext
        self.ub_ext = ub_ext
        self.lut_ext = lut_ext
        self.lut_up_ext = lut_up_ext
        self.oob_ext = oob_ext
        self.feasible_solutions = feasible_solutions


# Sort options of results
class SortOption(Enum):
    delta2 = 1
    start_delta1 = 2
    final_delta1 = 3
    elementary = 4
    exceeded = 5
    iterations = 6

