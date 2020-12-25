from controller.FileController import FileController
import unittest


class TestFileController(unittest.TestCase):

    def test_isPathValid_ValidPath_ShouldReturnTrue(self):
        path = './resources/data.csv'
        file_controller = FileController()

        actual = file_controller.is_path_valid(path)
        self.assertTrue(actual)

    def test_isPathValid_InvalidPath_ShouldReturnFalse(self):
        path = 'What shall we do with a drunken sailor?'
        file_controller = FileController()

        actual = file_controller.is_path_valid(path)
        self.assertFalse(actual)

    def test_isPathValid_None_ShouldReturnFalse(self):
        path = None
        file_controller = FileController()

        actual = file_controller.is_path_valid(path)
        self.assertFalse(actual)

    def test_isPathValid_InvalidType_ShouldReturnFalse(self):
        path = 42
        file_controller = FileController()

        actual = file_controller.is_path_valid(path)
        self.assertFalse(actual)
