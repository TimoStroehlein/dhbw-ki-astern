from model.Node import Node


class Link:
    """
    Represents link/ path between two rooms/ nodes..
    :param node1: The first node of the link.
    :param node2: The second node of the link.
    :param is_door: Whether the link is a door or not.
    :param is_door: Whether the link is open or not.
    :param is_door: Whether the link is a sentinel or not.
    :param is_door: Whether the link is a ladder or not.
    """
    def __init__(self, node1: Node, node2: Node, is_door, is_open, is_sentinel, is_ladder):
        self.node1 = node1
        self.node2 = node2
        self.is_door = is_door
        self.is_open = is_open
        self.is_sentinel = is_sentinel
        self.is_ladder = is_ladder

    def __str__(self):
        """ Return object as string """
        return '%s, %s, %d, %d, %d, %d' % (
                self.node1, self.node2, self.is_door, self.is_open, self.is_sentinel, self.is_ladder)
