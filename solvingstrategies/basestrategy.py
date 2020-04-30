class BaseStrategy:
    def __init__(self, board):
        self.board = board

    def apply_strategy(self, values, constraints):
        pass

    def apply(self):
        for row, constraints in enumerate(self.board.get_row_constraints()):
            res = self.apply_strategy(self.board.get_row(row), constraints)
            for col, val in enumerate(res):
                self.board.set_position(col, row, val)
        for col, constraints in enumerate(self.board.get_col_constraints()):
            res = self.apply_strategy(self.board.get_column(col), constraints)
            for row, val in enumerate(res):
                self.board.set_position(col, row, val)
