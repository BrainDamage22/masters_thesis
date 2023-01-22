class Node:
    def __init__(self, number, x, y):
        self.number = number
        self.x = x
        self.y = y


class NodeWithNeighbours(Node):
    def __init__(self, number, x, y, neighbours):
        self.neighbours = neighbours
        Node.__init__(self, number, x, y)


class IterationResult:
    def __init__(self, best_route, min_cost, sub_tours, cardinality, delta1, delta2, exceeded):
        self.best_route = best_route
        self.min_cost = min_cost
        self.sub_tours = sub_tours
        self.cardinality = cardinality
        self.delta1 = delta1
        self.delta2 = delta2
        self.exceeded = exceeded
