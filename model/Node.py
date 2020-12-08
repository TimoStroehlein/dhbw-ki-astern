class Node:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.f = 0     # Total cost of the node: f = g + h
        self.g = 0     # Cost of from the start node to this node
        self.h = 0     # Estimate the cost from the current node to the destination node
