from unittest import TestCase
from unittest.mock import patch, mock_open
from nonogramsolver.board import BoardWriter, Board


class TestBoardWriter(TestCase):
    def setUp(self):
        self.board = Board(4, 3, [[1, 2], [1, 1], []], [[1, 1], [], [2], [2]])
        self.board.set_position(0, 0, Board.Cross)
        self.board.set_position(2, 1, Board.Empty)

    @patch('builtins.open', new_callable=mock_open, create=True)
    def test_write_board_success(self, mock_file):
        BoardWriter(self.board).export('open/path/file.json')
        mock_file.assert_called_once_with('open/path/file.json', 'w')
        mock_file().write.assert_called_with(
            '{"width": 4, "height": 3, "constraints": {"rows": [[1, 2], [1, 1], []], '
            '"columns": [[1, 1], [], [2], [2]]}, '
            '"values": [{"x": 0, "y": 0, "value": true}, {"x": 1, "y": 2, "value": false}]}'
        )
