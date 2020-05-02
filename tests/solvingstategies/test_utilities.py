from unittest import TestCase
from solvingstrategies.utilities import Utilities
from board import Board


class TestUtilities(TestCase):
    def test_all_blocks_present(self):
        self.assertTrue(Utilities.all_blocks_present([Board.Cross], [1]))
        self.assertFalse(Utilities.all_blocks_present([], [1]))
        self.assertFalse(Utilities.all_blocks_present([Board.Empty], [1]))
        self.assertFalse(Utilities.all_blocks_present([Board.Cross, Board.Empty, Board.Empty], [1, 1]))
        self.assertFalse(Utilities.all_blocks_present([Board.Unknown, Board.Unknown, Board.Cross, Board.Unknown,
                                                       Board.Cross, Board.Unknown, Board.Unknown], [1, 3]))
        self.assertTrue(Utilities.all_blocks_present([Board.Unknown, Board.Unknown, Board.Cross, Board.Unknown,
                                                      Board.Cross, Board.Cross, Board.Unknown], [1, 3]))
        self.assertTrue(Utilities.all_blocks_present([Board.Unknown, Board.Unknown, Board.Cross, Board.Empty,
                                                      Board.Cross, Board.Unknown, Board.Unknown], [1, 3]))
        self.assertTrue(Utilities.all_blocks_present([Board.Cross, Board.Empty, Board.Cross, Board.Unknown,
                                                      Board.Unknown], [1, 3]))
        self.assertTrue(Utilities.all_blocks_present([Board.Unknown, Board.Cross, Board.Unknown, Board.Cross], [2, 1]))

    def test_get_positions_of_scores(self):
        self.assertListEqual(Utilities.get_positions_of_scores([]), [])
        self.assertListEqual(Utilities.get_positions_of_scores([Board.Unknown]), [])
        self.assertListEqual(Utilities.get_positions_of_scores([Board.Cross]), [(0, 0)])
        self.assertListEqual(Utilities.get_positions_of_scores([Board.Empty]), [])
        self.assertListEqual(Utilities.get_positions_of_scores([Board.Cross, Board.Empty, Board.Cross]),
                             [(0, 0), (2, 2)])
        self.assertListEqual(Utilities.get_positions_of_scores([Board.Cross, Board.Cross, Board.Cross]), [(0, 2)])
        self.assertListEqual(Utilities.get_positions_of_scores([Board.Cross, Board.Unknown, Board.Cross]),
                             [(0, 0), (2, 2)])
        self.assertListEqual(Utilities.get_positions_of_scores([Board.Unknown, Board.Cross, Board.Empty]), [(1, 1)])

    def test_get_unknown_positions(self):
        self.assertListEqual(Utilities.get_unknown_positions([]), [])
        self.assertListEqual(Utilities.get_unknown_positions([Board.Unknown]), [(0, 0)])
        self.assertListEqual(Utilities.get_unknown_positions([Board.Cross]), [])
        self.assertListEqual(Utilities.get_unknown_positions([Board.Empty]), [])
        self.assertListEqual(Utilities.get_unknown_positions([Board.Cross, Board.Empty, Board.Cross]), [])
        self.assertListEqual(Utilities.get_unknown_positions([Board.Unknown, Board.Unknown, Board.Unknown]), [(0, 2)])
        self.assertListEqual(Utilities.get_unknown_positions([Board.Cross, Board.Unknown, Board.Cross]), [(1, 1)])
        self.assertListEqual(Utilities.get_unknown_positions([Board.Unknown, Board.Cross, Board.Unknown]),
                             [(0, 0), (2, 2)])

    def test_constraint_fit_in_unknown(self):
        unknown_pos = Utilities.get_unknown_positions([Board.Unknown, Board.Unknown, Board.Cross, Board.Unknown,
                                                       Board.Empty, Board.Cross, Board.Cross, Board.Unknown])
        self.assertFalse(Utilities.constraint_fit_in_unknown(3, unknown_pos, 0, 2))
        self.assertTrue(Utilities.constraint_fit_in_unknown(2, unknown_pos, 0, 2))
        self.assertFalse(Utilities.constraint_fit_in_unknown(2, unknown_pos, 1, 2))
        self.assertTrue(Utilities.constraint_fit_in_unknown(1, unknown_pos, 0, 0))
        self.assertFalse(Utilities.constraint_fit_in_unknown(2, unknown_pos, 0, 0))
        self.assertTrue(Utilities.constraint_fit_in_unknown(1, unknown_pos, 0, 7))
        self.assertFalse(Utilities.constraint_fit_in_unknown(8, unknown_pos, 0, 7))
        self.assertFalse(Utilities.constraint_fit_in_unknown(2, unknown_pos, 3, 4))
