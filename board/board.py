from exceptions import InvalidValueError


class Board:
    """
    The Board class represents a board of a nonogram game.
    """

    Unknown = 0  # for values we do not yet know
    Cross = 1
    Empty = 2

    def __init__(self, width, height, row_constraints, col_constraints):
        """
        Constructor for a board.
        :param width: The width of the board.
        :param height: The height of the board.
        :param row_constraints: List of list of integers to represent the row constraints.
        :param col_constraints: List of list of integers to represent the col constraints.
        """
        self._width = width
        self._height = height
        self._board = [[Board.Unknown] * width for _ in range(height)]
        self._row_constraints = row_constraints
        self._col_constraints = col_constraints

    def set_position(self, col, row, value):
        """
        Sets the given position to the given value.
        :param col: Column index to set.
        :param row: Row index to set.
        :param value: The value to set.
        :raise: InvalidValueError: If the value was illegal.
        """
        if value in [Board.Unknown, Board.Cross, Board.Empty]:
            self._board[row][col] = value
        else:
            raise InvalidValueError(
                'Value {} is invalid for position ({}, {})'.format(
                    value, col, row
                )
            )

    def get_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def get_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_row_constraints(self):
        """
        Get the list of list of integers that represent the row constraints.
        """
        return self._row_constraints

    def get_col_constraints(self):
        """
        Get the list of list of integers that represent the col constraints.
        """
        return self._col_constraints

    def get_value(self, col, row):
        """
        Get the value of the board at the given position.
        :param col: The requested column index.
        :param row: The requested row index.
        :return: The value of the board at the given position.
        """
        return self._board[row][col]

    def get_row(self, index):
        """
        Get the row at the given index.
        :param index: The requested index of the row.
        :return: A list of values representing the row at the given index.
        """
        return self._board[index]

    def get_column(self, index):
        """
        Get the column at the given index.
        :param index: The requesteed index of the column.
        :return: A list of values representing the column at the given index.
        """
        return [row[index] for row in self._board]

    @staticmethod
    def get_score(values):
        """
        Calculates the score of the given array of values.
        The score is represented by a list of integers: each "block" of crosses is represented in that list by the
        length of that block.
        :param values: The array of values to get the score of.
        :return: A list of integers representing the score.
        """
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

    def _get_row_score(self, index):
        """
        Get the score of a certain row.
        :param index: The index of the row.
        :return: The score of the row.
        """
        return Board.get_score(self.get_row(index))

    def _get_column_score(self, index):
        """
        Get the score of a certain column.
        :param index: The index of the column.
        :return: The score of the column.
        """
        return Board.get_score(self.get_column(index))

    def check_correct(self):
        """
        Check if a board is correct with the current values.
        A board is correct when all of the constraints are met.
        :return: True if the board is correct, False otherwise.
        """
        for i, constraint in enumerate(self._row_constraints):
            if self._get_row_score(i) != constraint:
                return False
        for i, constraint in enumerate(self._col_constraints):
            if self._get_column_score(i) != constraint:
                return False
        return True
