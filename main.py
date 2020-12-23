import argparse
import logging
import sys
import time

from model.Node import Node
from controller.FileController import FileController
from controller.AStarController import AStarController


def main():
    # Argument parser that handles the cli arguments
    parser = argparse.ArgumentParser(
        description='A program to to find the shortest path with A*.')

    # Each argument is handled differently
    parser.add_argument("-v", "--verbose",
                        help="Show info messages while running",
                        action="store_const",
                        dest="log_level",
                        const=logging.INFO)
    parser.add_argument("-d", "--debug",
                        help="Show detailed debug messages while running",
                        action="store_const",
                        dest="log_level",
                        const=logging.DEBUG)
    parser.add_argument("-i", "--import",
                        help="Import the data from a file",
                        action="store",
                        dest="import_path",
                        required=True)
    parser.add_argument("-e", "--export",
                        help="Export the result to a file",
                        action="store",
                        dest="export_path")

    # Parse all passed arguments
    args = parser.parse_args()
    # Handle the log level
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=args.log_level)
    if args.log_level == logging.DEBUG:
        logging.warning("Running in debug mode! Console outputs may be large.")

    # Start the import and path calculation
    start(args)


def start(args):
    """
    Start the import and path calculation.
    """
    # Set the start node
    start_node = Node((15, -4, 6))
    dest_node = Node((0, 0, 0))  # End node is the center of the cube

    # Read the data from the csv file
    file_controller = FileController()
    logging.info('Importing data from %s...', args.import_path)
    links, nodes = file_controller.import_file(args.import_path, start_node, dest_node)
    logging.info('Successfully imported data from %s!', args.import_path)

    # Calculate the path
    a_star_controller = AStarController(links, nodes, start_node, dest_node)
    logging.info('Starting path search...')
    start_time = time.perf_counter()
    cheapest_path = a_star_controller.search_path()
    end_time = time.perf_counter()
    if cheapest_path:
        logging.info('Cheapest path successfully found in %.3f ms!' %
                     ((end_time - start_time) * 1000))
        if args.export_path:
            logging.info('Exporting result to: %s' % args.export_path)
            file_controller.export_file(args.export_path, cheapest_path)
            logging.info('Result successfully exported!')
        sys.exit(0)
    else:
        logging.fatal('Cheapest path could not be found.')
        sys.exit(1)


if __name__ == '__main__':
    main()
