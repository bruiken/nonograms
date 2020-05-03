from nonogramsolver.board.board import Board
from json import loads


class BoardReader:
    def __init__(self, path):
        self.path = path

    def _get_board_data(self):
        with open(self.path, 'r') as f:
            return loads(f.read())

    def get_board(self):
        data = self._get_board_data()
        board = Board(data['width'], data['height'],
                      data['constraints']['rows'],
                      data['constraints']['columns'])
        for val in data['values']:
            board_val = Board.Cross if val['value'] else Board.Empty
            board.set_position(val['x'], val['y'], board_val)
        return board
