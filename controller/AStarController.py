import itertools

from model.Link import Link
from model.Node import Node


class AStartController:
    def __init__(self, links, nodes, start_node: Node, dest_node: Node):
        self.links = links
        self.nodes = nodes
        self.start_node = start_node
        self.dest_node = dest_node

    def start_search(self):
        # Initialization
        self.start_node.g = 0
        self.h(self.start_node)
        self.start_node.f = self.start_node.g + self.start_node.h
        self.start_node.tritanium_blaster = 12
        self.start_node.energy_units = 12
        open_list = [self.start_node]  # Open list, contains the start node at the beginning
        closed_list = []  # Closed list, contains all already visited nodes

        # Iterate through all nodes until every node has been visited or the destination node has not been reached
        while open_list:
            # Sort the open list to get the lowest f score node first
            open_list.sort()

            # Pop current node off the open list and add it to the closed list
            current_node = open_list.pop(0)
            closed_list.append(current_node)

            # Finish if the current node is the destination node
            if current_node == self.dest_node:
                # Destroying the vinculum costs 5 minutes, with a tritanium-blaster 1 minute
                if current_node.tritanium_blaster >= 1:
                    current_node.g = current_node.g + 1
                    current_node.f = current_node.g + current_node.h
                    current_node.tritanium_blaster = current_node.tritanium_blaster - 1
                else:
                    current_node.g = current_node.g + 5
                    current_node.f = current_node.g + current_node.h

                # Reconstruct the path
                path = self.reconstruct_path(current_node)
                print('Destination reached, cost: %f' % current_node.f)
                for node in path:
                    print(node)
                exit(0)

            # Get all links to the child nodes
            links = []
            nodes = []
            for link in self.links:
                if link.node1 == current_node:
                    links.append(link)
                    nodes.append(link.node2)
                elif link.node2 == current_node:
                    links.append(link)
                    nodes.append(link.node1)

            # Get all possible neighbours on the same level and below, that could be opened with a tritanium blaster

            # Iterate through all children
            current_link: Link
            child_node: Node
            for current_link, child_node in itertools.zip_longest(links, nodes):
                # Continue if node of the link is in the closed list
                if child_node in closed_list:
                    continue

                # Calculate the f, g and h values
                if self.g(current_link, current_node, child_node):
                    self.h(child_node)
                    child_node.f = child_node.g + child_node.h
                    child_node.parent_node = current_node

                    # Check if the child node is already in the open list
                    if any(child_node == open_node for open_node in open_list):
                        continue

                    # Append the child node to the open list
                    open_list.append(child_node)

    def g(self, link: Link, current_node: Node, child_node: Node):
        # TODO: Implement blasting a hole in a wall or ground
        # Blasting a hole in a wall with a tritanium-blaster costs 3 minutes, can be used in all directions expect up

        # Determine whether the current or new g value is cheaper
        def is_cheaper(cost, tritanium_blaster_cost=0, energy_unit_cost=0):
            if child_node.g < current_node.g + cost:
                return False
            elif child_node.g == current_node.g + cost:
                tritanium_blaster = child_node.tritanium_blaster - current_node.tritanium_blaster\
                                    + tritanium_blaster_cost
                energy_units = child_node.energy_units - current_node.energy_units + energy_unit_cost
                # Current node has more tritanium blaster and energy units combined
                if (tritanium_blaster + energy_units) < 0:
                    return True
                # Current node hase less tritanium blaster and energy units combined
                else:
                    return False
            else:
                return True

        # Path with or without a drone
        if link.is_open:
            # Destroying a drone costs 3 minutes and one energy unit
            # 5 minute regeneration time before a new drone can be fought
            if link.is_sentinel:
                if current_node.energy_units == 0:
                    return False
                # Check whether a regeneration is set or not, if so, take a brake
                # A 1 minute Break can always be used and repeated
                if current_node.regeneration_time == 0:
                    if not is_cheaper(3, energy_unit_cost=1):
                        return False
                    child_node.g = current_node.g + 3
                    child_node.parent_link_type = 'drone'
                else:
                    if not is_cheaper(3 + current_node.regeneration_time, energy_unit_cost=1):
                        return False
                    child_node.g = current_node.g + 3 + current_node.regeneration_time
                    child_node.parent_link_type = 'drone & %f minutes regeneration' % current_node.regeneration_time

                child_node.energy_units = current_node.energy_units - 1
                child_node.regeneration_time = 5
                child_node.tritanium_blaster = current_node.tritanium_blaster
            # No obstacle, costs 1 minute
            else:
                if not is_cheaper(1):
                    return False
                child_node.g = current_node.g + 1
                child_node.regeneration_time = current_node.regeneration_time - 1
                child_node.tritanium_blaster = current_node.tritanium_blaster
                child_node.energy_units = current_node.energy_units
                child_node.parent_link_type = 'open'

        # Costs 2 minutes
        elif link.is_door:
            if not is_cheaper(2):
                return False
            child_node.g = current_node.g + 2
            child_node.regeneration_time = current_node.regeneration_time - 2
            child_node.tritanium_blaster = current_node.tritanium_blaster
            child_node.energy_units = current_node.energy_units
            child_node.parent_link_type = 'door'

        # Up the ladder costs 2 minutes
        # Down costs 1/2 minute
        elif link.is_ladder:
            # Check if the ladder has been went up or down
            if current_node.position[2] <= child_node.position[2]:
                if not is_cheaper(2, energy_unit_cost=2):
                    return False
                child_node.g = current_node.g + 2
                child_node.regeneration_time = current_node.regeneration_time - 2
                child_node.parent_link_type = 'ladder up'
            else:
                if not is_cheaper(0.5, energy_unit_cost=2):
                    return False
                child_node.g = current_node.g + 0.5
                child_node.regeneration_time = current_node.regeneration_time - 0.5
                child_node.parent_link_type = 'ladder down'

            child_node.tritanium_blaster = current_node.tritanium_blaster
            child_node.energy_units = current_node.energy_units

        return True

    # Estimate the cost of the cheapest path from the next node to the destination node
    def h(self, child_node: Node):
        (x1, y1, z1) = child_node.position
        (x2, y2, z2) = self.dest_node.position
        child_node.h = abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)

    def reconstruct_path(self, current_node: Node):
        path = [current_node]
        while current_node != self.start_node:
            current_node = current_node.parent_node
            path.append(current_node)
        # Return reversed path
        return path[::-1]
