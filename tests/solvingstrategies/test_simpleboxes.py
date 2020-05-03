from unittest import TestCase
from nonogramsolver.solvingstrategies import SimpleBoxes
from nonogramsolver.board import Board


class TestSimpleBoxes(TestCase):
    def test_strategy(self):
        self.assertListEqual(SimpleBoxes.apply_strategy(None, [Board.Unknown], [1]), [Board.Cross])
        self.assertListEqual(SimpleBoxes.apply_strategy(None, [Board.Unknown], []), [Board.Unknown])
        self.assertListEqual(SimpleBoxes.apply_strategy(None, [Board.Empty], [1]), [Board.Empty])
        self.assertListEqual(SimpleBoxes.apply_strategy(None, [Board.Unknown, Board.Unknown, Board.Unknown], [2]),
                             [Board.Unknown, Board.Cross, Board.Unknown])
        self.assertListEqual(SimpleBoxes.apply_strategy(None, [Board.Unknown, Board.Empty, Board.Unknown], [1, 1]),
                             [Board.Unknown, Board.Empty, Board.Unknown])
        self.assertListEqual(SimpleBoxes.apply_strategy(None, [Board.Unknown] * 6, [1, 4]),
                             [Board.Unknown, Board.Unknown, Board.Cross, Board.Cross, Board.Unknown, Board.Unknown])
