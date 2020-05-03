from unittest import TestCase
from nonogramsolver.board import Board
from nonogramsolver.exceptions import InvalidValueError


class TestBoard(TestCase):
    def test_static_values(self):
        self.assertEqual(Board.Unknown, 0)
        self.assertEqual(Board.Cross, 1)
        self.assertEqual(Board.Empty, 2)

    def setUp(self):
        self.row_constaints = [
            [1, 2, 3],
            [],
            [3, 2, 1],
            []
        ]
        self.col_constraints = [
            [4, 2],
            [],
            [2, 4]
        ]
        self.board = Board(3, 4, self.row_constaints, self.col_constraints)

    def test_width_height(self):
        self.assertEqual(self.board.get_width(), 3)
        self.assertEqual(self.board.get_height(), 4)

    def test_constraints(self):
        self.assertListEqual(self.row_constaints, self.board.get_row_constraints())
        self.assertListEqual(self.col_constraints, self.board.get_col_constraints())

    def test_set_value(self):
        self.board.set_position(0, 0, Board.Empty)
        self.assertEqual(self.board._board[0][0], Board.Empty)
        with self.assertRaises(InvalidValueError):
            self.board.set_position(1, 1, 3)
        self.board.set_position(2, 3, Board.Cross)
        self.assertEqual(self.board._board[3][2], Board.Cross)
        self.board.set_position(2, 3, Board.Unknown)
        self.assertEqual(self.board._board[3][2], Board.Unknown)

    def test_get_value(self):
        self.board._board[0][0] = Board.Empty
        self.assertEqual(self.board.get_value(0, 0), Board.Empty)
        self.board._board[3][2] = Board.Cross
        self.assertEqual(self.board.get_value(2, 3), Board.Cross)
        self.board._board[3][2] = Board.Unknown
        self.assertEqual(self.board.get_value(2, 3), Board.Unknown)

    def test_default_unknown(self):
        self.assertListEqual(self.board._board, [[Board.Unknown] * 3 for _ in range(4)])

    def test_get_row_col(self):
        self.board.set_position(1, 1, Board.Cross)
        self.board.set_position(1, 0, Board.Cross)
        self.assertListEqual(self.board.get_row(0), [Board.Unknown, Board.Cross, Board.Unknown])
        self.assertListEqual(self.board.get_row(1), [Board.Unknown, Board.Cross, Board.Unknown])
        self.assertListEqual(self.board.get_row(2), [Board.Unknown, Board.Unknown, Board.Unknown])
        self.assertListEqual(self.board.get_row(3), [Board.Unknown, Board.Unknown, Board.Unknown])
        self.assertListEqual(self.board.get_column(0), [Board.Unknown, Board.Unknown, Board.Unknown, Board.Unknown])
        self.assertListEqual(self.board.get_column(1), [Board.Cross, Board.Cross, Board.Unknown, Board.Unknown])
        self.assertListEqual(self.board.get_column(2), [Board.Unknown, Board.Unknown, Board.Unknown, Board.Unknown])

    def test_get_score(self):
        self.assertListEqual(Board.get_score([]), [])
        self.assertListEqual(Board.get_score([Board.Unknown]), [])
        self.assertListEqual(Board.get_score([Board.Empty]), [])
        self.assertListEqual(Board.get_score([Board.Cross]), [1])
        self.assertListEqual(Board.get_score([Board.Cross, Board.Empty, Board.Cross, Board.Cross, Board.Unknown]),
                             [1, 2])
        self.assertListEqual(Board.get_score([Board.Cross, Board.Cross, Board.Cross, Board.Cross]), [4])

    def test_check_correct(self):
        simple_board = Board(1, 1, [[]], [[]])
        self.assertTrue(simple_board.check_correct())
        simple_board.set_position(0, 0, Board.Empty)
        self.assertTrue(simple_board.check_correct())
        simple_board.set_position(0, 0, Board.Cross)
        self.assertFalse(simple_board.check_correct())
        self.assertFalse(self.board.check_correct())
        board = Board(4, 2, [[1, 2], [3]], [[1], [1], [2], [2]])
        self.assertFalse(board.check_correct())
        board.set_position(0, 0, Board.Cross)
        board.set_position(2, 0, Board.Cross)
        board.set_position(3, 0, Board.Cross)
        board.set_position(1, 1, Board.Cross)
        board.set_position(2, 1, Board.Cross)
        board.set_position(3, 1, Board.Cross)
        self.assertTrue(board.check_correct())
