from unittest import TestCase
from nonogramsolver.solvingstrategies import SimpleSpaces
from nonogramsolver.board import Board


class TestSimpleSpaces(TestCase):
    def test_strategy(self):
        self.assertListEqual(SimpleSpaces.apply_strategy(None, [Board.Unknown], []), [Board.Empty])
        self.assertListEqual(SimpleSpaces.apply_strategy(None, [Board.Empty], []), [Board.Empty])
        self.assertListEqual(SimpleSpaces.apply_strategy(None, [Board.Cross], []), [Board.Cross])
        self.assertListEqual(SimpleSpaces.apply_strategy(None, [Board.Unknown], [1]), [Board.Unknown])
        self.assertListEqual(SimpleSpaces.apply_strategy(None, [Board.Cross, Board.Unknown, Board.Cross], [1, 1]),
                             [Board.Cross, Board.Empty, Board.Cross])
        self.assertListEqual(SimpleSpaces.apply_strategy(None, [Board.Unknown, Board.Unknown, Board.Cross,
                                                                Board.Unknown, Board.Cross, Board.Cross], [2, 2]),
                             [Board.Empty, Board.Unknown, Board.Cross, Board.Unknown, Board.Cross, Board.Cross])
        self.assertListEqual(SimpleSpaces.apply_strategy(None, [Board.Unknown, Board.Unknown, Board.Cross,
                                                                Board.Unknown, Board.Unknown, Board.Cross, Board.Cross],
                                                         [3, 3]),
                             [Board.Unknown, Board.Unknown, Board.Cross, Board.Unknown, Board.Unknown, Board.Cross,
                              Board.Cross])
