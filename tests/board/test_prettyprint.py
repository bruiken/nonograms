from unittest import TestCase
from nonogramsolver.board import PrintBoard, Board


class TestPrintBoard(TestCase):
    def setUp(self):
        self.board1 = Board(2, 2, [[], [1]], [[1], []])
        self.board2 = Board(5, 6, [[1, 2, 3], [4, 5], [], [7], [4, 2], []],
                            [[1, 1, 1, 1, 1, 6], [], [1, 2, 3], [], [1]])
        self.board3 = Board(1, 1, [[]], [[]])

    def test_print1(self):
        board1_str = PrintBoard(self.board1)._print()
        self.assertEqual(board1_str, '    1   \n   ====\n  ǁ ? ?\n1 ǁ ? ?\n')
        self.board1.set_position(0, 1, Board.Cross)
        board1_str = PrintBoard(self.board1)._print()
        self.assertEqual(board1_str, '    1   \n   ====\n  ǁ ? ?\n1 ǁ X ?\n')
        self.board1.set_position(0, 0, Board.Empty)
        self.board1.set_position(1, 0, Board.Empty)
        self.board1.set_position(1, 1, Board.Empty)
        board1_str = PrintBoard(self.board1)._print()
        self.assertEqual(board1_str, '    1   \n   ====\n  ǁ    \n1 ǁ X  \n')

    def test_print2(self):
        board2_str = PrintBoard(self.board2)._print()
        self.assertEqual(board2_str, '        1         \n        1         \n        1         \n        1   1     \n'
                                     '        1   2     \n        6   3   1 \n       ==========\n1 2 3 ǁ ? ? ? ? ?\n'
                                     '  4 5 ǁ ? ? ? ? ?\n      ǁ ? ? ? ? ?\n    7 ǁ ? ? ? ? ?\n  4 2 ǁ ? ? ? ? ?\n'
                                     '      ǁ ? ? ? ? ?\n')

    def test_print3(self):
        board3_str = PrintBoard(self.board3)._print()
        self.assertEqual(board3_str, ' ==\nǁ ?\n')
