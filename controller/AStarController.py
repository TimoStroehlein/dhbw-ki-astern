import itertools
import logging

from model.Link import Link
from model.Node import Node


class AStartController:
    """
    Calculates the shortest/ cheapest path with the A* algorithm.
    :param links: Links of the graph.
    :param nodes: Nodes of the graph.
    :param start_node: Start node of the graph, where the algorithm should start.
    :param dest_node: Destination node of the graph.
    """
    def __init__(self, links, nodes, start_node: Node, dest_node: Node):
        self.links = links
        self.nodes = nodes
        self.start_node = start_node
        self.dest_node = dest_node

    def search_path(self, log_level):
        """
        Start the A* search algorithm.
        :return: Successful or not successful, if successful, then return the cheapest path and cost.
        """
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
            current_node: Node = open_list.pop(0)
            closed_list.append(current_node)
            logging.debug('current_node: ' + str(current_node))

            # Finish if the current node is the destination node
            path = self.is_finished(current_node)
            if path:
                return path

            # Get all child links and nodes
            links, nodes = self.get_child_nodes(current_node)

            # Get all possible neighbours on the same level and below, that could be opened with a tritanium blaster
            neighbour_list = self.get_neighbors(current_node.position)
            neighbour: Node
            for neighbour in neighbour_list:
                if neighbour not in nodes:
                    nodes.append(neighbour)

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
                    if child_node in open_list:
                        continue

                    # Append the child node to the open list
                    open_list.append(child_node)

        return False

    def g(self, current_link: Link, current_node: Node, child_node: Node):
        """
        Calculate the cost/ distance from start to the child node.
        :param current_link: Current link from the current node to the child node.
        :param current_node: Current parent node.
        :param child_node: Child node of the current node.
        :return: Whether the g score could be set or not.
        """
        # No link to the neighbor room, link can be blasted
        # Blasting a hole in a wall with a tritanium-blaster costs 3 minutes, can be used in all directions expect up
        if current_link is None:
            if not self.is_cheaper(current_node, child_node, 3):
                return False
            child_node.g = current_node.g + 3
            child_node.regeneration_time = current_node.regeneration_time - 3
            child_node.tritanium_blaster = current_node.tritanium_blaster - 1
            child_node.energy_units = current_node.energy_units
            child_node.parent_link_type = 'wall or ground blasted'
            return True

        # Path with or without a drone
        if self.is_open(current_node, child_node, current_link):
            return True

        # Door costs 2 minutes
        if self.is_door(current_node, child_node, current_link):
            return True

        # Up the ladder costs 2 minutes
        # Down costs 1/2 minute
        if self.is_ladder(current_node, child_node, current_link):
            return True

        return False

    @staticmethod
    def is_cheaper(current_node: Node, child_node: Node, cost, tritanium_blaster_cost=0, energy_unit_cost=0):
        """
        Determine whether the current or new g value is cheaper.
        :param current_node: The current node.
        :param child_node: The child node of the current node.
        :param cost: Cost from the current to the child node.
        :param tritanium_blaster_cost: Tritanium blaster cost from current to child node.
        :param energy_unit_cost: Energy unit cost from current to child node.
        :return: Whether the path is cheaper or not.
        """
        if child_node.g < current_node.g + cost:
            return False
        if child_node.g == current_node.g + cost:
            tritanium_blaster = child_node.tritanium_blaster - current_node.tritanium_blaster \
                                + tritanium_blaster_cost
            energy_units = child_node.energy_units - current_node.energy_units + energy_unit_cost
            # True: Current node has more tritanium blaster and energy units combined
            # False: Current node hase less tritanium blaster and energy units combined
            return (tritanium_blaster + energy_units) < 0
        return True

    def is_open(self, current_node: Node, child_node: Node, current_link: Link):
        """
        Check whether the link is open and the path is cheaper.
        Path with or without a drone.
        :param current_node: The current node.
        :param child_node:  The child node of the current node.
        :param current_link:  The link from the current to the child node.
        :return: Whether the link is open and cheaper or not.
        """
        if current_link.is_open:
            # Destroying a drone costs 3 minutes and one energy unit
            # 5 minute regeneration time before a new drone can be fought
            if current_link.is_sentinel:
                # Check if any energy units are left
                if current_node.energy_units == 0:
                    return False
                # Check whether a regeneration is set or not, if so, take a brake
                # A 1 minute Break can always be used and repeated
                if current_node.regeneration_time == 0:
                    if not self.is_cheaper(current_node, child_node, 3, energy_unit_cost=1):
                        return False
                    child_node.g = current_node.g + 3
                    child_node.parent_link_type = 'drone'
                else:
                    if not self.is_cheaper(current_node, child_node, 3 + current_node.regeneration_time,
                                           energy_unit_cost=1):
                        return False
                    child_node.g = current_node.g + 3 + current_node.regeneration_time
                    child_node.parent_link_type = 'drone & %f minutes regeneration' % current_node.regeneration_time

                child_node.energy_units = current_node.energy_units - 1
                child_node.regeneration_time = 5
                child_node.tritanium_blaster = current_node.tritanium_blaster
            # No obstacle, costs 1 minute
            else:
                if not self.is_cheaper(current_node, child_node, 1):
                    return False
                child_node.g = current_node.g + 1
                child_node.regeneration_time = current_node.regeneration_time - 1
                child_node.tritanium_blaster = current_node.tritanium_blaster
                child_node.energy_units = current_node.energy_units
                child_node.parent_link_type = 'open'
            return True
        return False

    def is_door(self, current_node: Node, child_node: Node, current_link: Link):
        """
        Check whether the link is a door and the path is cheaper.
        Door costs 2 minutes.
        :param current_node: The current node.
        :param child_node:  The child node of the current node.
        :param current_link:  The link from the current to the child node.
        :return: Whether the link is a door and cheaper or not.
        """
        if current_link.is_door:
            if not self.is_cheaper(current_node, child_node, 2):
                return False
            child_node.g = current_node.g + 2
            child_node.regeneration_time = current_node.regeneration_time - 2
            child_node.tritanium_blaster = current_node.tritanium_blaster
            child_node.energy_units = current_node.energy_units
            child_node.parent_link_type = 'door'
            return True
        return False

    def is_ladder(self, current_node: Node, child_node: Node, current_link: Link):
        """
        Check whether the link is a ladder and the path is cheaper.
        Up the ladder costs 2 minutes.
        Down costs 1/2 minute.
        :param current_node: The current node.
        :param child_node:  The child node of the current node.
        :param current_link:  The link from the current to the child node.
        :return: Whether the link is a ladder and cheaper or not.
        """
        if current_link.is_ladder:
            # Check if the ladder has been went up or down
            if current_node.position[2] <= child_node.position[2]:
                if not self.is_cheaper(current_node, child_node, 2, energy_unit_cost=2):
                    return False
                child_node.g = current_node.g + 2
                child_node.regeneration_time = current_node.regeneration_time - 2
                child_node.parent_link_type = 'ladder up'
            else:
                if not self.is_cheaper(current_node, child_node, 0.5, energy_unit_cost=2):
                    return False
                child_node.g = current_node.g + 0.5
                child_node.regeneration_time = current_node.regeneration_time - 0.5
                child_node.parent_link_type = 'ladder down'

            child_node.tritanium_blaster = current_node.tritanium_blaster
            child_node.energy_units = current_node.energy_units
            return True
        return False

    def is_finished(self, current_node: Node):
        """
        Finish if the current node is the destination node.
        :param current_node: The current node.
        :return: If the path has been found or not, if so, return the cheapest path.
        """
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
            for node in path:
                logging.debug(node)
            logging.info('Destination reached, final cost: %f' % current_node.g)
            return path
        return False

    def h(self, child_node: Node):
        """
        Estimate the cost of the cheapest path from the next node to the destination node.
        Calculate the heuristic.
        :param child_node: Child node from where the heuristic should be calculated.
        """
        (x1, y1, z1) = child_node.position
        (x2, y2, z2) = self.dest_node.position
        child_node.h = abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)

    def reconstruct_path(self, current_node: Node):
        """
        Reconstruct the cheapest path with backtracking.
        :param current_node: Current node from where the path should be backtracked.
        :return: Reversed path.
        """
        path = [current_node]
        while current_node != self.start_node:
            current_node = current_node.parent_node
            path.append(current_node)
        # Return reversed path
        return path[::-1]

    def get_child_nodes(self, current_node: Node):
        """
        Get all links to the child nodes.
        :param current_node: The current node.
        :return: Child links and nodes.
        """
        links = []
        nodes = []
        for link in self.links:
            if link.node1 == current_node:
                links.append(link)
                nodes.append(link.node2)
            elif link.node2 == current_node:
                links.append(link)
                nodes.append(link.node1)
        return links, nodes

    def get_neighbors(self, position):
        """
        Get all neighbours of the current room, also those without a link.
        :param position: Tuple position of the node.
        :return: Neighbor of the node.
        """
        neighbors = []
        (x, y, z) = position
        candidates = [(x - 1, y, z), (x + 1, y, z), (x, y - 1, z), (x, y + 1, z), (x, y, z - 1)]
        for candidate in candidates:
            try:
                found_node = next(filter(lambda node, pos=candidate: node.position == pos, self.nodes), None)
                if found_node:
                    neighbors.append(found_node)
            except IndexError:
                logging.warning("IndexError in get_neighbors at candidate ", candidate)
                pass
        return neighbors
