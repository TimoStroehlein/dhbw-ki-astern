class Node:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.f = 0     # Total cost of the node: f = g + h
        self.g = 0     # Cost of from the start node to this node
        self.h = 0     # Estimate the cost from the current node to the destination node
        self.tritanium_blaster = 0     # Used to open a wall/ ground and destroy the vinculum faster
        self.energy_units = 0          # Used to fight drones

    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        return '%d, %d, %d' % (self.x, self.y, self.z)
