class Node:
    def __init__(self, number, x, y):
        self.number = number
        self.x = x
        self.y = y


class NodeWithNeighbours(Node):
    def __init__(self, number, x, y, neighbours):
        self.neighbours = neighbours
        Node.__init__(self, number, x, y)
