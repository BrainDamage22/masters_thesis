class Node:
    def __init__(self, number, x, y):
        self.number = number
        self.x = x
        self.y = y


class NodeWithNeighbours(Node):
    def __init__(self, number, x, y, neighbours):
        self.neighbours = neighbours
        Node.__init__(self, number, x, y)


class Route:
    def __init__(self, startingNode):
        self.costs = 0
        self.path = [startingNode]
