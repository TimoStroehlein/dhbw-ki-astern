import logging
import os
import csv
import sys

from model.Link import Link
from model.Node import Node


class FileController:
    """
    Import the graph from a csv file.
    """
    def __init__(self):
        self.links = []
        self.nodes = []

    def import_file(self, import_path, start_node: Node, dest_node: Node):
        """
        Read the csv file from the given import path.
        :param start_node: Start node of the graph.
        :param dest_node: Destination node of the graph.
        :param import_path: Path to the csv file.
        :return: Links and nodes from the csv file.
        """
        # If the import path is not valid, exit
        if not self.is_path_valid(import_path):
            sys.exit(2)

        # Add the start and dest nodes to the nodes list
        self.nodes.append(start_node)
        self.nodes.append(dest_node)

        # Starting the import
        with open(import_path) as csv_file:
            # Iterate through each row
            reader = csv.reader(csv_file, delimiter=';')
            for i, row in enumerate(reader):
                if i == 0:
                    continue
                # Get the nodes
                node1 = Node((int(row[0] or '0'), int(row[1] or '0'), int(row[2] or '0')))
                node2 = Node((int(row[3] or '0'), int(row[4] or '0'), int(row[5] or '0')))
                # Add the nodes, if they haven't been added yet
                found_node = next((node for node in self.nodes if node1 == node), None)
                if found_node:
                    node1 = found_node
                else:
                    self.nodes.append(node1)
                found_node = next((node for node in self.nodes if node2 == node), None)
                if found_node:
                    node2 = found_node
                else:
                    self.nodes.append(node2)
                # Add the link
                self.links.append(Link(node1, node2, int(row[6] or '0'), int(row[7] or '0'),
                                  int(row[8] or '0'), int(row[9] or '0')))

        # Print the file if debug is enabled
        self.print_file()
        return self.links, self.nodes

    def print_file(self):
        """ Print the file to the console """
        logging.debug('Data imported:')
        for link in self.links:
            logging.debug(str(link))

    @staticmethod
    def export_file(export_path, cheapest_path: []):
        """
        Export the result to a given file.
        :param export_path: Path to the file, where the result should be stored.
        :param cheapest_path: Cheapest path from the start to the destination node.
        """
        file = open(export_path, 'w')
        for node in cheapest_path:
            file.write(str(node) + '\n')
        file.write('Cost: %f' % cheapest_path[len(cheapest_path)-1].g)
        file.close()

    @staticmethod
    def is_path_valid(path):
        """
        Checks if the passed path is valid.
        :param path: The path to check.
        :return: Boolean: True on valid, false on invalid.
        """
        # If path is empty, it is not a valid path
        if path is None:
            return False

        # Check if the file exists and that it is accessible
        try:
            if os.path.exists(path):
                file = open(path, 'r')  # Opening with write deletes the file contents!
                file.close()
                return True
            return False
        except OSError:
            # Cannot open the file
            logging.error('The path \'%s\' is not a valid path or the file does not exist.' % path)
            return False
        except TypeError:
            # Path is not of type string or os.path, should never happen
            logging.error('Path is in an invalid type! Aborting file access.')
            return False
