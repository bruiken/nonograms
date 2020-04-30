from board.board import Board
from json import dumps


class BoardWriter:
    def __init__(self, board):
        self.board = board

    def export(self, path):
        data = self._create_data_dict()
        with open(path, 'w') as f:
            f.write(dumps(data))

    def _create_data_dict(self):
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
        result = []
        for row in range(self.board.get_width()):
            for col in range(self.board.get_height()):
                value = self.board.get_value(col, row)
                if value != Board.Unknown:
                    result.append({
                        'x': col,
                        'y': row,
                        'value': value == Board.Cross
                    })
        return result
