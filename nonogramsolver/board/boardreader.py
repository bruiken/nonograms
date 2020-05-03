from nonogramsolver.board.board import Board
from json import loads
from nonogramsolver.exceptions import InvalidBoardFile


class BoardReader:
    """
    A board reader that reads a board from a json file. The json file needs to be structured as follows:
    {
        "width": int,
        "height": int,
        "constraints": {
            "columns": [[int]],
            "rows": [[int]]
        },
        "values": [
            {
                "x": int,
                "y": int,
                "value": bool  // true -> cross, false -> empty
            }
        ]
    }
    """

    def __init__(self, path):
        """
        Constructor for a BoardReader.
        :param path: The path to the .json file.
        """
        self.path = path

    def _get_board_data(self):
        """
        Gets the board data from the given file.
        :return: a dictionary representation of the data in the file.
        """
        with open(self.path, 'r') as f:
            return loads(f.read())

    def get_board(self):
        """
        Get a Board instance that represents the board in the given file.
        :return: The Board of the file.
        :raise: InvalidBoardFile: If there is a field missing in the file.
        """
        data = self._get_board_data()
        try:
            board = Board(data['width'], data['height'], data['constraints']['rows'], data['constraints']['columns'])
            for val in data['values']:
                board_val = Board.Cross if val['value'] else Board.Empty
                board.set_position(val['x'], val['y'], board_val)
            return board
        except KeyError as e:
            raise InvalidBoardFile('The file does not contain the value \'{}\''.format(e.args[0]))
