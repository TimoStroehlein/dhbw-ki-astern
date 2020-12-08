import logging
import os
import csv

from model.Link import Link


class FileController:

    links = []

    @classmethod
    def read_file(cls, import_path, export_path=None):
        # Check import path is not valid, exit
        if not cls.is_path_valid(import_path):
            exit(2)

        # Starting the import
        logging.info('Importing data from %s...', import_path)
        with open(import_path) as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            for i, row in enumerate(reader):
                if i == 0:
                    continue
                cls.links.append(Link(int(row[0] or '0'), int(row[1] or '0'), int(row[2] or '0'), int(row[3] or '0'),
                                      int(row[4] or '0'), int(row[5] or '0'), int(row[6] or '0'), int(row[7] or '0'),
                                      int(row[8] or '0'), int(row[9] or '0')))

        # Print the file if debug is enabled
        logging.debug('Data imported:')
        cls.print_file()

        return cls.links

    @classmethod
    def print_file(cls):
        for link in cls.links:
            print('%d, %d, %d, %d, %d, %d, %d, %d, %d, %d' % (
                  link.x1, link.y1, link.z1, link.x2, link.y2, link.z2,
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
