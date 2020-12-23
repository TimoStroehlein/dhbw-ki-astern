import unittest
from controller.AStarController import AStarController
from controller.FileController import FileController
from model.Node import Node


class ValidationUtility(unittest.TestCase):
    """
    Parent Class for all validation unit tests.
    Contains utility needed to set up validation tests.
    """

    astar_controller = None

    @classmethod
    def set_up_test_method(cls, filename, start_node, dest_node, blaster=12, energy=12):
        # Set up the controller with the validation example
        path = './validation/resources/%s.csv' % filename
        file_controller = FileController()
        links, nodes = file_controller.import_file(path, start_node, dest_node)
        cls.astar_controller = AStarController(links, nodes, start_node, dest_node, blaster, energy)