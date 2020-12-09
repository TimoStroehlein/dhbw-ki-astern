import sys


class Node:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.f = sys.maxsize    # Total cost of the node: f = g + h
        self.g = sys.maxsize    # Cost of from the start node to this node
        self.h = sys.maxsize    # Estimate the cost from the current node to the destination node
        self.parent_node = None         # Parent node used for cheapest path
        self.parent_link_type = None
        self.tritanium_blaster = 0      # Used to open a wall/ ground and destroy the vinculum faster
        self.energy_units = 0           # Used to fight drones
        self.regeneration_time = 0      # 5 minutes regeneration time after fighting a drone

    @property
    def _regeneration_time(self):
        return self.regeneration_time

    @_regeneration_time.setter
    def _regeneration_time(self, value):
        if value < 0:
            self.regeneration_time = 0
        else:
            self.regeneration_time = value

    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        return '%d, %d, %d' % (self.x, self.y, self.z)
