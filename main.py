import argparse
import logging
import csv

from controller.FileController import FileController


def read_file(import_path, export_path=None):
    file_controller = FileController()

    # Check import path is not valid, exit
    if not file_controller.is_path_valid(import_path):
        exit(2)

    # Starting the import
    logging.info('Importing data from %s...', import_path)
    with open(import_path) as csv_file:
        spam_reader = csv.reader(csv_file, delimiter=';')
        for row in spam_reader:
            print(', '.join(row))


def main():
    # Argument parser that handles the cli arguments
    parser = argparse.ArgumentParser(
        description='A program to to find the shortest path with A*.'
    )

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

    # Handle the import and export arguments
    if args.import_path:
        if args.export_path:
            read_file(args.import_path, args.export_path)
        else:
            read_file(args.import_path)


if __name__ == '__main__':
    main()
