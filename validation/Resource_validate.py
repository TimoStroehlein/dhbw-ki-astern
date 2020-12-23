from validation.AStarValidation import AStarValidation
from model.Node import Node


class ValidateRouting(AStarValidation):

    def test_DestroyWithBlaster_ShouldTakeOneMinute(self):
        AStarValidation.set_up_test_method('destroy', Node((0, 0, 0)))

        expected = 1
        result = AStarValidation.astar_controller.search_path()
        actual = result[len(result) - 1].g  # get the final cost

        self.assertEqual(expected, actual)

    def test_DestroyWithoutBlaster_ShouldTakeFiveMinute(self):
        AStarValidation.set_up_test_method('destroy', Node((0, 0, 0)), blaster=0)

        expected = 5
        result = AStarValidation.astar_controller.search_path()
        actual = result[len(result) - 1].g  # get the final cost

        self.assertEqual(expected, actual)

    def test_UseEnergy_ShouldReduceEnergyCount(self):
        AStarValidation.set_up_test_method('energy', Node((2, 0, 0)), energy=2)

        expected = 0
        result = AStarValidation.astar_controller.search_path()
        actual = result[len(result) - 1].energy_units  # get the final energy unit count

        self.assertEqual(expected, actual)

    def test_UseBlaster_ShouldReduceBlasterCount(self):
        AStarValidation.set_up_test_method('blasting', Node((2, 0, 0)), blaster=1)

        expected = 0
        result = AStarValidation.astar_controller.search_path()
        actual = result[len(result) - 1].tritanium_blaster  # get the final tritanium blaster count

        self.assertEqual(expected, actual)

