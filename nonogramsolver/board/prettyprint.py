from nonogramsolver.board.board import Board


class PrintBoard:
    def __init__(self, board):
        self.board = board

    def print(self):
        col_consts = self.board.get_col_constraints()
        row_consts = self.board.get_row_constraints()
        max_row_const = max(len(x) for x in row_consts)
        max_col_const = max(len(x) for x in col_consts)
        result = ''
        for cc_idx in range(max_col_const):
            result += ' ' * (2 * max_row_const + 2)
            for col in range(self.board.get_width()):
                if len(col_consts[col]) >= max_col_const - cc_idx:
                    result += str(col_consts[col][len(col_consts[col]) - cc_idx - 1]) + ' '
                else:
                    result += '  '
            result += '\n'
        result += ' ' * (2 * max_row_const + 1) + '=' * (2 * self.board.get_width()) + '\n'
        for row in range(self.board.get_height()):
            result += '  ' * (max_row_const - len(row_consts[row])) + ' '.join(str(x) for x in row_consts[row]) + ' ǁ'
            for v in self.board.get_row(row):
                result += ' '
                if v == Board.Empty:
                    result += ' '
                elif v == Board.Unknown:
                    result += '?'
                elif v == Board.Cross:
                    result += 'X'
            result += '\n'
        print(result)
