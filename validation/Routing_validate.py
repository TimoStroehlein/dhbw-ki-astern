from validation.AStarValidation import AStarValidation
from model.Node import Node


class ValidateResources(AStarValidation):
    """
    Unit tests for validating the routing of the A* algorithm.
    Caluclates times for bigger systems and for simple links (door, open, ladders, sentinel)

    Test method names should show you all info to understand what the test does:
    test_[function to validate]_[Expected result]
    """

    def test_Search_ShouldTakeCheaperPath(self):
        AStarValidation.set_up_test_method('cheapest', Node((2, 0, 0)), Node((0, 0, 0)))
        # cheaper.csv has shortest path of cost 6
        # cost 3 through open doors
        # cost 2 through closed door
        # cost 1 to destroy
        expected = 6
        result = AStarValidation.astar_controller.search_path()
        actual = result[len(result) - 1].g  # get the final cost

        self.assertEqual(expected, actual)

    def test_Search_ShouldTakePathOfLeastResistance(self):
        # IMPLEMENT
        self.fail()

    def test_SearchNotPossible_ShouldReturnFalse(self):
        AStarValidation.set_up_test_method('impossible', Node((2, 0, 0)), Node((0, 0, 0)))

        result = AStarValidation.astar_controller.search_path()

        self.assertFalse(result)

    def test_LadderUp_ShouldTakeTwo(self):
        AStarValidation.set_up_test_method('simple_links', Node((0, 0, -1)), Node((0, 0, 0)))

        # cost 2 through ladder up
        # cost 1 to destroy
        expected = 3
        result = AStarValidation.astar_controller.search_path()
        actual = result[len(result) - 1].g  # get the final cost

        self.assertEqual(expected, actual)

    def test_LadderDown_ShouldTakePointFive(self):
        AStarValidation.set_up_test_method('simple_links', Node((0, 0, 1)), Node((0, 0, 0)))

        # cost 0.5 through ladder down
        # cost 1 to destroy
        expected = 1.5
        result = AStarValidation.astar_controller.search_path()
        actual = result[len(result) - 1].g  # get the final cost

        self.assertEqual(expected, actual)

    def test_Open_ShouldTakeOne(self):
        AStarValidation.set_up_test_method('simple_links', Node((0, 1, 0)), Node((0, 0, 0)))

        # cost 1 through open
        # cost 1 to destroy
        expected = 2
        result = AStarValidation.astar_controller.search_path()
        actual = result[len(result) - 1].g  # get the final cost

        self.assertEqual(expected, actual)

    def test_Door_ShouldTakeTwo(self):
        AStarValidation.set_up_test_method('simple_links', Node((1, 0, 0)), Node((0, 0, 0)))

        # cost 2 through door
        # cost 1 to destroy
        expected = 3
        result = AStarValidation.astar_controller.search_path()
        actual = result[len(result) - 1].g  # get the final cost

        self.assertEqual(expected, actual)

    def test_BlastWall_ShouldTakeThree(self):
        AStarValidation.set_up_test_method('blasting', Node((1, 0, 0)), Node((0, 0, 0)))

        # cost 3 to blast through wall
        # cost 1 to destroy
        expected = 4
        result = AStarValidation.astar_controller.search_path()
        actual = result[len(result) - 1].g  # get the final cost

        self.assertEqual(expected, actual)
