import unittest
from controller.AStarController import AStarController
from controller.FileController import FileController
from model.Node import Node


class ValidationUtility(unittest.TestCase):
    """
    Parent Class for all validation unit tests.
    Contains utility needed to set up validation tests.
    """

    a_star_controller = None

    @classmethod
    def set_up_test_method(cls, filename, start_node, dest_node, blaster=12, energy=12):
        """
        Sets up a test method with variable parameters, differing by test case. Replaces a undynamic setUp method by the
        unittest package, which would set up every method with the same parameters.
        :param filename: name of the file in /validation/resources to import
        :param start_node: At what node the algorithm should be started
        :param dest_node: At what node the algorithm should finish
        :param blaster: Blaster amount at the start of the algorithm
        :param energy: Energy amount at the start of the algorithm
        :return: Sets the class variable a_star_controller with an initialized AStarController instance
        """
        path = './validation/resources/%s.csv' % filename
        file_controller = FileController()
        links, nodes = file_controller.import_file(path, start_node, dest_node)
        cls.a_star_controller = AStarController(links, nodes, start_node, dest_node, blaster,
                                                energy)
