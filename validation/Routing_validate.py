from validation.ValidationUtility import ValidationUtility
from model.Node import Node


class ValidateRouting(ValidationUtility):
    """
    Unit tests for validating the routing of the A* algorithm.
    Calculates times for bigger systems and for simple links (door, open, ladders, sentinel)

    Test method names should show you all info to understand what the test does:
    test_[function to validate]_[Expected result]
    """

    def test_Search_ShouldTakeCheaperPath(self):
        ValidationUtility.set_up_test_method('cheapest', Node((2, 0, 0)), Node((0, 0, 0)))
        # cheaper.csv has shortest path of cost 6
        # cost 3 through open doors
        # cost 2 through closed door
        # cost 1 to destroy
        expected = 12
        result = ValidationUtility.a_star_controller.search_path()
        actual = result[len(result) - 1].g  # get the final cost

        self.assertEqual(expected, actual)

    def test_LeastResistance_ShouldHaveTwelveEnergyUnits(self):
        ValidationUtility.set_up_test_method('least_resistance', Node((3, 0, 0)), Node((0, 0, 0)))

        # least_resistance.csv has shortest path of cost 13
        # path with least resistance is door (5x2) and open (1x1)
        # path of same length is sentinel(3)-wait(5)-sentinel(3)
        # energy_units should be unchanged because path of least resistance is taken
        expected = 12
        result = ValidationUtility.a_star_controller.search_path()
        actual = result[len(result) - 1].energy_units  # get the final cost

        self.assertEqual(expected, actual)

    def test_SearchNotPossible_ShouldReturnFalse(self):
        ValidationUtility.set_up_test_method('impossible', Node((2, 0, 0)), Node((0, 0, 0)))

        result = ValidationUtility.a_star_controller.search_path()

        self.assertFalse(result)

    def test_LadderUp_ShouldCostTwo(self):
        ValidationUtility.set_up_test_method('simple_links', Node((0, 0, -1)), Node((0, 0, 0)))

        # cost 2 through ladder up
        # cost 1 to destroy
        expected = 3
        result = ValidationUtility.a_star_controller.search_path()
        actual = result[len(result) - 1].g  # get the final cost

        self.assertEqual(expected, actual)

    def test_LadderDown_ShouldCostPointFive(self):
        ValidationUtility.set_up_test_method('simple_links', Node((0, 0, 1)), Node((0, 0, 0)))

        # cost 0.5 through ladder down
        # cost 1 to destroy
        expected = 1.5
        result = ValidationUtility.a_star_controller.search_path()
        actual = result[len(result) - 1].g  # get the final cost

        self.assertEqual(expected, actual)

    def test_Open_ShouldCostOne(self):
        ValidationUtility.set_up_test_method('simple_links', Node((0, 1, 0)), Node((0, 0, 0)))

        # cost 1 through open
        # cost 1 to destroy
        expected = 2
        result = ValidationUtility.a_star_controller.search_path()
        actual = result[len(result) - 1].g  # get the final cost

        self.assertEqual(expected, actual)

    def test_Door_ShouldCostTwo(self):
        ValidationUtility.set_up_test_method('simple_links', Node((1, 0, 0)), Node((0, 0, 0)))

        # cost 2 through door
        # cost 1 to destroy
        expected = 3
        result = ValidationUtility.a_star_controller.search_path()
        actual = result[len(result) - 1].g  # get the final cost

        self.assertEqual(expected, actual)

    def test_BlastWall_ShouldCostThree(self):
        ValidationUtility.set_up_test_method('blasting', Node((1, 0, 0)), Node((0, 0, 0)))

        # cost 3 to blast through wall
        # cost 1 to destroy
        expected = 4
        result = ValidationUtility.a_star_controller.search_path()
        actual = result[len(result) - 1].g  # get the final cost

        self.assertEqual(expected, actual)
