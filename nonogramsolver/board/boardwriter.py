from nonogramsolver.board.board import Board
from json import dumps


class BoardWriter:
    """
    The board writer can write a current state of a Board to a json file that can later be read again by the
    BoardReader.
    """

    def __init__(self, board):
        """
        Constructor for a BoardWriter.
        :param board: The Board that will be written to file.
        """
        self.board = board

    def export(self, path):
        """
        Exports the board to the given file.
        :param path: The path where to save the file.
        """
        data = self._create_data_dict()
        with open(path, 'w') as f:
            f.write(dumps(data))

    def _create_data_dict(self):
        """
        Creates a dictionary that can later be exported to json.
        :return: A dictionary containing the board data.
        """
        return {
            'width': self.board.get_width(),
            'height': self.board.get_height(),
            'constraints': {
                'rows': self.board.get_row_constraints(),
                'columns': self.board.get_col_constraints()
            },
            'values': self._create_values_dict()
        }

    def _create_values_dict(self):
        """
        Creates a dictionary of the current values on the board.
        Only the Empty and Cross values will be saved as Unknown is the default.
        :return: A dictionary that represents the values on the board.
        """
        result = []
        for row in range(self.board.get_width()):
            for col in range(self.board.get_height()):
                value = self.board.get_value(row, col)
                if value != Board.Unknown:
                    result.append({'x': col, 'y': row, 'value': value == Board.Cross})
        return result
