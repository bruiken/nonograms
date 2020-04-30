from exceptions import InvalidValueError


class Board:
    Unknown = 0
    Cross = 1
    Empty = 2

    def __init__(self, width, height, row_constraints, col_constraints):
        self._width = width
        self._height = height
        self._board = [[Board.Unknown] * width for _ in range(height)]
        self._row_constraints = row_constraints
        self._col_constraints = col_constraints

    def set_position(self, col, row, value):
        if value in [Board.Unknown, Board.Cross, Board.Empty]:
            self._board[row][col] = value
        else:
            raise InvalidValueError(
                'Value {} is invalid for position ({}, {})'.format(
                    value, col, row
                )
            )

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_row_constraints(self):
        return self._row_constraints

    def get_col_constraints(self):
        return self._col_constraints

    def get_value(self, col, row):
        return self._board[row][col]

    def get_row(self, index):
        return self._board[index]

    def get_column(self, index):
        return [row[index] for row in self._board]

    @staticmethod
    def get_score(values):
        result = []
        count = 0
        for val in values:
            if val != Board.Cross and count > 0:
                result.append(count)
                count = 0
            elif val == Board.Cross:
                count += 1
        if count > 0:
            result.append(count)
        return result

    def get_row_score(self, index):
        return Board.get_score(self.get_row(index))

    def get_column_score(self, index):
        return Board.get_score(self.get_column(index))

    def check_correct(self):
        for i, constraint in enumerate(self._row_constraints):
            if self.get_row_score(i) != constraint:
                return False
        for i, constraint in enumerate(self._col_constraints):
            if self.get_column_score(i) != constraint:
                return False
        return True
