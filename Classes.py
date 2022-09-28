class Node:
    def __init__(self, number, x, y, z):
        self.number = number
        self.x = x
        self.y = y
        self.z = z


class NodeWithRoutes:
    def __init__(self, number, x, y, z):
        self.number = number
        self.x = x
        self.y = y
        self.z = z

    routes = []
