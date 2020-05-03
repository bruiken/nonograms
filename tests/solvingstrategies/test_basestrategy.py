from unittest import TestCase
from unittest.mock import MagicMock
from nonogramsolver.solvingstrategies.basestrategy import BaseStrategy
from nonogramsolver.board import Board


class TestBaseStrategy(TestCase):
    def setUp(self):
        self.board = Board(3, 4, [[], [], [], []], [[], [], []])

    def test_apply(self):
        bs = BaseStrategy(self.board)
        bs.apply_strategy = MagicMock()
        bs.apply()
        self.assertEqual(bs.apply_strategy.call_count, self.board.get_height() + self.board.get_width())

    def test_apply_change_board(self):
        bs = BaseStrategy(self.board)
        bs.apply_strategy = lambda values, _: [Board.Cross] * len(values)
        bs.apply()
        self.assertListEqual(self.board._board, [[Board.Cross] * 3 for _ in range(4)])
