from nonogramsolver.board.board import Board


class PrintBoard:
    def __init__(self, board):
        self.board = board
        self.col_consts = [list(reversed(x)) for x in self.board.get_col_constraints()]
        self.row_consts = self.board.get_row_constraints()
        self.max_row_const = max(len(x) for x in self.row_consts)
        self.max_col_const = max(len(x) for x in self.col_consts)

    def print(self):
        """
        Print the board to the console.
        """
        print(self._print())
    def _print(self):
        result = self._get_col_constraint_str()
        result += ' ' * (2 * self.max_row_const + 1) + '=' * (2 * self.board.get_width()) + '\n'
        result += self._get_rows_str()
        return result
        result = ''
        for cc_idx in range(self.max_col_const):
            result += ' ' * (2 * self.max_row_const + 2)
            for col in range(self.board.get_width()):
                if len(self.col_consts[col]) >= self.max_col_const - cc_idx:
                    result += str(self.col_consts[col][self.max_col_const - cc_idx - 1]) + ' '
                else:
                    result += '  '
            result += '\n'
        return result

    def _get_rows_str(self):
        result = ''
        for row in range(self.board.get_height()):
            result += '  ' * (self.max_row_const - len(self.row_consts[row])) + \
                      ' '.join(str(x) for x in self.row_consts[row]) + \
                      ' ' * (min(1, len(self.row_consts[row]))) + 'ǁ'
            result += self._get_row_str(row)
        return result

    def _get_row_str(self, row_idx):
        result = ''
        for v in self.board.get_row(row_idx):
            result += ' '
            if v == Board.Empty:
                result += ' '
            elif v == Board.Unknown:
                result += '?'
            elif v == Board.Cross:
                result += 'X'
        return result + '\n'
