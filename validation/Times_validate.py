from validation.ValidationUtility import ValidationUtility
from model.Node import Node


class ValidateTimes(ValidationUtility):
    """
    Unit tests for validating the timers of the A* algorithm.
    Validates that cooldowns and regeneration times are calculated correctly.

    Test method names should show you all info to understand what the test does:
    test_[function to validate]_[Expected result]
    """

    def test_EnergyCooldown_ShouldRegardCooldownOfFive(self):
        ValidationUtility.set_up_test_method('energy', Node((2, 0, 0)), Node((0, 0, 0)))

        # cost 3 through sentinel hallway
        # cost 5 for cooldown (wait)
        # cost 3 through sentinel hallway
        # cost 1 to destroy
        expected = 12
        result = ValidationUtility.a_star_controller.search_path()
        actual = result[len(result) - 1].g  # get the final cost

        self.assertEqual(expected, actual)

    def test_RegenerationDoor_ShouldReduceRegenerationTimeByTwo(self):
        ValidationUtility.set_up_test_method('regeneration_door', Node((2, 0, 0)), Node((0, 0, 0)))

        # regeneration time at 5
        # door takes 2
        # destroy takes 1
        expected = 2
        result = ValidationUtility.a_star_controller.search_path()
        actual = result[len(result) - 1].regeneration_time  # get the final cost

        self.assertEqual(expected, actual)

    def test_RegenerationOpen_ShouldReduceRegenerationTimeByOne(self):
        ValidationUtility.set_up_test_method('regeneration_open', Node((1, 1, 0)), Node((0, 0, 0)))

        # regeneration time at 5
        # open takes 1
        # destroy takes 1
        expected = 3
        result = ValidationUtility.a_star_controller.search_path()
        actual = result[len(result) - 1].regeneration_time  # get the final cost

        self.assertEqual(expected, actual)

    def test_RegenerationLadderUp_ShouldReduceRegenerationTimeByTwo(self):
        ValidationUtility.set_up_test_method('regeneration_ladder_up', Node((1, 0, -1)),
                                             Node((0, 0, 0)))

        # regeneration time at 5
        # ladder up takes 2
        # destroy takes 1
        expected = 2
        result = ValidationUtility.a_star_controller.search_path()
        actual = result[len(result) - 1].regeneration_time  # get the final cost

        self.assertEqual(expected, actual)

    def test_RegenerationLadderDown_ShouldReduceRegenerationTimeByPointFive(self):
        ValidationUtility.set_up_test_method('regeneration_ladder_down', Node((1, 0, 1)),
                                             Node((0, 0, 0)))

        # regeneration time at 5
        # ladder down takes 0.5
        # destroy takes 1
        expected = 3.5
        result = ValidationUtility.a_star_controller.search_path()
        actual = result[len(result) - 1].regeneration_time  # get the final cost

        self.assertEqual(expected, actual)

    def test_RegenerationBlastWall_ShouldReduceRegenerationTimeByThree(self):
        ValidationUtility.set_up_test_method('regeneration_blasting', Node((2, 0, 0)),
                                             Node((0, 0, 0)))

        # regeneration time at 5
        # blast wall takes 3
        # destroy takes 1
        expected = 1
        result = ValidationUtility.a_star_controller.search_path()
        actual = result[len(result) - 1].regeneration_time  # get the final cost

        self.assertEqual(expected, actual)
