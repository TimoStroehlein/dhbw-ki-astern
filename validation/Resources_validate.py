from validation.ValidationUtility import ValidationUtility
from model.Node import Node


class ValidateResources(ValidationUtility):
    """
    Unit tests for validating the resource management of the A* algorithm.
    Calculates times and resource counts for energy units and tritanium blasters.

    Test method names should show you all info to understand what the test does:
    test_[function to validate]_[Expected result]
    """

    def test_DestroyWithBlaster_ShouldCostOne(self):
        ValidationUtility.set_up_test_method('destroy', Node((0, 0, 0)), Node((0, 0, 0)))

        expected = 1
        result = ValidationUtility.a_star_controller.search_path()
        actual = result[len(result) - 1].g  # get the final cost

        self.assertEqual(expected, actual)

    def test_DestroyWithoutBlaster_ShouldCostFive(self):
        ValidationUtility.set_up_test_method('destroy', Node((0, 0, 0)), Node((0, 0, 0)), blaster=0)

        expected = 5
        result = ValidationUtility.a_star_controller.search_path()
        actual = result[len(result) - 1].g  # get the final cost

        self.assertEqual(expected, actual)

    def test_UseEnergy_ShouldReduceEnergyCount(self):
        ValidationUtility.set_up_test_method('energy', Node((2, 0, 0)), Node((0, 0, 0)), energy=2)

        expected = 0
        result = ValidationUtility.a_star_controller.search_path()
        actual = result[len(result) - 1].energy_units  # get the final energy unit count

        self.assertEqual(expected, actual)

    def test_UseBlaster_ShouldReduceBlasterCount(self):
        ValidationUtility.set_up_test_method('blasting', Node((1, 0, 0)), Node((0, 0, 0)),
                                             blaster=1)

        expected = 0
        result = ValidationUtility.a_star_controller.search_path()
        actual = result[len(result) - 1].tritanium_blaster  # get the final tritanium blaster count

        self.assertEqual(expected, actual)
