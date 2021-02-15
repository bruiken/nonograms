class BaseStrategy:
    """
    Base stategy to be extended by actual strategies.
    Strategies have to implement the apply_strategy function.
    """

    def __init__(self, board):
        """
        Constructor for a BaseStrategy.
        :param board: The board on which the strategy will be applied.
        """
        self.board = board

    def apply_strategy(self, values, constraints):
        """
        The apply strategy function applies the strategy on an array of values
        with their corresponding constraints.
        The function should return the new array of values that is created by
        the strategy.
        :param values: The array of values to apply the stategy on.
        :param constraints: The constraints to apply the strategy on.
        :return: The new array of values resulting from the strategy.
        """
        pass

    def apply(self):
        """
        Applies the strategy on the whole board.
        This calls the apply_strategy function on each row and column with
        their respective constraints.
        It sets the new values on the board as well (resulting from the
        apply_strategy function).
        """
        for row, constraints in enumerate(self.board.get_row_constraints()):
            res = self.apply_strategy(self.board.get_row(row), constraints)
            for col, val in enumerate(res):
                self.board.set_position(col, row, val)
        for col, constraints in enumerate(self.board.get_col_constraints()):
            res = self.apply_strategy(self.board.get_column(col), constraints)
            for row, val in enumerate(res):
                self.board.set_position(col, row, val)
