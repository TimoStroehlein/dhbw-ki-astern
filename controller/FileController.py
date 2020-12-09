import logging
import os
import csv

from model.Link import Link
from model.Node import Node


class FileController:
    links = []
    nodes = []

    @classmethod
    def read_file(cls, import_path, export_path=None, log_level=None):
        # Check import path is not valid, exit
        if not cls.is_path_valid(import_path):
            exit(2)

        counter = 0

        # Starting the import
        logging.info('Importing data from %s...', import_path)
        with open(import_path) as csv_file:
            # Iterate through each row
            reader = csv.reader(csv_file, delimiter=';')
            for i, row in enumerate(reader):
                if i == 0:
                    continue

                # Get the nodes
                node1 = Node(int(row[0] or '0'), int(row[1] or '0'), int(row[2] or '0'))
                node2 = Node(int(row[3] or '0'), int(row[4] or '0'), int(row[5] or '0'))

                # Add the nodes, if they haven't been added yet
                found_node = next((node for node in cls.nodes if node1 == node), None)
                if found_node:
                    node1 = found_node
                else:
                    cls.nodes.append(node1)
                found_node = next((node for node in cls.nodes if node2 == node), None)
                if found_node:
                    node2 = found_node
                else:
                    cls.nodes.append(node2)

                # Add the link
                cls.links.append(Link(node1, node2, int(row[6] or '0'), int(row[7] or '0'),
                                      int(row[8] or '0'), int(row[9] or '0')))

        # Print the file if debug is enabled
        if log_level == logging.DEBUG:
            logging.debug('Data imported:')
            cls.print_file()

        return cls.links, cls.nodes

    @classmethod
    def print_file(cls):
        for link in cls.links:
            print('%s, %s, %d, %d, %d, %d' % (
                (link.node1.x, link.node1.y, link.node1.z), (link.node2.x, link.node2.y, link.node2.z),
                link.is_door, link.is_open, link.is_sentinel, link.is_ladder))

    @classmethod
    def is_path_valid(cls, path):
        """
        Checks if the passed path is valid
        :param path: The path to check
        :return: Boolean: True on valid, false on invalid
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
            else:
                return False
        except OSError:
            # Cannot open the file
            print('[ERROR] The path \'', path, '\' is not a valid path or the file does not exist.')
            return False
        except TypeError:
            # Path is not of type string or os.path, should never happen
            print("[FATAL] Path is in an invalid type!")
            return False
