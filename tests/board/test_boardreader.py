from unittest import TestCase
from unittest.mock import patch, mock_open
from nonogramsolver.exceptions import InvalidBoardFile
from nonogramsolver.board import BoardReader, Board


class TestBoardReader(TestCase):
    correct_file = """
    {
        "width": 4,
        "height": 3,
        "constraints": {
            "columns": [[1, 1], [], [2], [2]],
            "rows": [[1, 2], [1, 1], []]
        },
        "values": [
            {"x": 0, "y": 0, "value": true},
            {"x": 2, "y": 1, "value": false}
        ]
    }
    """

    @patch('builtins.open', new_callable=mock_open, read_data='{ }')
    def test_get_board_fail(self, mock_file):
        with self.assertRaises(InvalidBoardFile):
            BoardReader('open/path/file.json').get_board()
        mock_file.assert_called_once_with('open/path/file.json', 'r')

    @patch('builtins.open', new_callable=mock_open, read_data=correct_file)
    def test_get_board_success(self, mock_file):
        board = BoardReader('open/path/file.json').get_board()
        mock_file.assert_called_once_with('open/path/file.json', 'r')
        self.assertEqual(board.get_width(), 4)
        self.assertEqual(board.get_height(), 3)
        self.assertListEqual(board.get_col_constraints(),
                             [[1, 1], [], [2], [2]])
        self.assertListEqual(board.get_row_constraints(), [[1, 2], [1, 1], []])
        self.assertEqual(board.get_value(0, 0), Board.Cross)
        self.assertEqual(board.get_value(2, 1), Board.Empty)
