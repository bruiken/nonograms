from nonogramsolver.board.board import Board


class PrintBoard:
    """
    Pretty print a board to the console.
    This currently only supports printing single digit constraints.
    """

    def __init__(self, board):
        """
        Constructor for a pretty printer.
        :param board: The board to be printed.
        """
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
        """
        Get the string that represents the board.
        :return: The string representing the board.
        """
        result = self._get_col_constraint_str()
        result += ' ' * (2 * self.max_row_const + 1) + '=' * (2 * self.board.get_width()) + '\n'
        result += self._get_rows_str()
        return result

    def _get_col_constraint_str(self):
        """
        Get the string that represents the column constraints.
        These are also correctly indented to account for the row constraints.
        :return: String that represents the column constraints.
        """
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
        """
        Get the string that represents all of the rows.
        :return: The string that represents the row constraints and the rows.
        """
        result = ''
        for row in range(self.board.get_height()):
            result += '  ' * (self.max_row_const - len(self.row_consts[row])) + \
                      ' '.join(str(x) for x in self.row_consts[row]) + \
                      ' ' * (min(1, len(self.row_consts[row]))) + 'ǁ'
            result += self._get_row_str(row)
        return result

    def _get_row_str(self, row_idx):
        """
        Get the string that represents one row.
        :param row_idx: The row that will be converted to string.
        :return: The string that represents the row at the given index.
        """
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
