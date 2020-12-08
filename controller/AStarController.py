from model.Link import Link
from model.Node import Node


class AStartController:
    def __init__(self, links, start_node: Node, dest_node: Node):
        self.links = links
        self.start_node = start_node
        self.dest_node = dest_node

    def start_search(self):
        self.start_node.f = self.start_node.g = self.start_node.h = 0
        open_list = [self.start_node]    # Open list, contains the start node at the beginning
        closed_list = []            # Closed list, contains all already visited nodes

        # Iterate through all nodes until every node has been visited or the destination node has not been reached
        while open_list:
            # Get the current node
            current_node = open_list[0]

            # Finish if the current node is the destination node
            if current_node == self.dest_node:
                exit(0)

            # Pop current node off the open list and add it to the closed list
            open_list.pop(0)
            closed_list.append(current_node)

            # Get all links to the child nodes
            links = []
            for link in self.links:
                if link.node1 == current_node:
                    links.append(link)

            # Iterate through all children
            current_link: Link
            for current_link in links:
                # Continue if node of the link is in the closed list
                for closed_child in closed_list:
                    if current_link.node2 == closed_child:
                        continue

                # Calculate the f, g and h values
                current_link.node2.g = self.g(current_link)
                current_link.node2.h = self.h(current_link.node2, self.dest_node)
                current_link.node2.f = self.f(current_node)

    def g(self, link: Link):
        # Blasting a wall costs 3 minutes, can be used in all directions expect up
        # A 1 minute Break can always be used and repeated
        # Destroying the vinculum costs 5 minutes, with a tritanium-blaster 1 minute
        # There are two dead soldiers with tritanium-balsters
        # TODO: Replace with real cost
        # No obstacle, costs 1 minute
        if link.is_open:
            return 1
        # Costs 2 minutes
        elif link.is_door:
            return 2
        # Drone costs 3 minutes and one energy unit
        # 5 minute regeneration time before a new drone can be fought
        elif link.is_sentinel:
            return 3
        # Up costs 2 minutes
        # Down costs 1/2 minute
        elif link.is_ladder:
            return 2
        return link.node1.g + 1

    # Estimate the cost of the cheapest path from the next node to the destination node
    def h(self, node1: Node, node2: Node):
        (x1, y1, z1) = node1
        (x2, y2, z2) = node2
        return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)

    def f(self, g, h): return g + h

    def reconstruct_path(self, start_node, current_node):
        # TODO: Calculate the path
        path = []
        return path
