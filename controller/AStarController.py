from model.Link import Link
from model.Node import Node


class AStartController:
    def __init__(self, links, start_node: Node, dest_node: Node):
        self.links = links
        self.start_node = start_node
        self.dest_node = dest_node

    def start_search(self):
        # Initialization
        self.start_node.f = self.start_node.g = self.start_node.h = 0
        self.start_node.tritanium_blaster = 12
        self.start_node.energy_units = 12
        open_list = [self.start_node]   # Open list, contains the start node at the beginning
        closed_list = []                # Closed list, contains all already visited nodes

        # Iterate through all nodes until every node has been visited or the destination node has not been reached
        while open_list:
            # Get the current node
            current_node = open_list[0]

            # Finish if the current node is the destination node
            if current_node == self.dest_node:
                # Destroying the vinculum costs 5 minutes, with a tritanium-blaster 1 minute
                cost = 1 if current_node.tritanium_blaster >= 1 else 5
                current_node.g = current_node.g + cost
                current_node.f = current_node.g + current_node.h
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
            print(str(current_node))
            current_link: Link
            for current_link in links:
                # Continue if node of the link is in the closed list
                for closed_child in closed_list:
                    if current_link.node2 == closed_child:
                        continue

                # Calculate the f, g and h values
                self.g(current_link)
                self.h(current_link, self.dest_node)
                self.f(current_link)

                # Check if the child node is already in the open list
                for open_node in open_list:
                    if current_link.node2 == open_node and current_link.node2.g > open_node.g:
                        continue

                # Append the child node to the open list
                open_list.append(current_link.node2)

    def g(self, link: Link):
        # Blasting a hole in a wall with a tritanium-blaster costs 3 minutes, can be used in all directions expect up
        # A 1 minute Break can always be used and repeated
        # TODO: Replace with real cost
        # No obstacle, costs 1 minute
        if link.is_open:
            link.node2.g = link.node1 + 1
        # Costs 2 minutes
        elif link.is_door:
            link.node2.g = link.node1 + 2
        # Destroying a drone costs 3 minutes and one energy unit
        # 5 minute regeneration time before a new drone can be fought
        elif link.is_sentinel:
            link.node2.g = link.node1.g + 3
            link.node2.energy_units = link.node2.energy_units - 1
        # Up the ladder costs 2 minutes
        # Down costs 1/2 minute
        elif link.is_ladder:
            if link.node1 <= link.node2:
                link.node2.g = link.node1.g + 2
            else:
                link.node2.g = link.node1.g + 0.5

    # Estimate the cost of the cheapest path from the next node to the destination node
    def h(self, current_link: Link, de: Node):
        (x1, y1, z1) = current_link.node2
        (x2, y2, z2) = self.dest_node
        current_link.node2.h = abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)

    def f(self, current_link: Link):
        current_link.node2.f = current_link.node2.g + current_link.node2.h

    def reconstruct_path(self, start_node, current_node):
        # TODO: Calculate the path and print it
        path = []
        return path
