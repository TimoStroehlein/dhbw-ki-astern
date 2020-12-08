from model.Node import Node


class Link:
    def __init__(self, node1: Node, node2: Node, is_door, is_open, is_sentinel, is_ladder):
        self.node1 = node1
        self.node2 = node2
        self.is_door = is_door
        self.is_open = is_open
        self.is_sentinel = is_sentinel
        self.is_ladder = is_ladder
