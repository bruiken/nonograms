from nonogramsolver.solvingstrategies.basestrategy import BaseStrategy
from nonogramsolver.solvingstrategies.utilities import Utilities


class JoiningSplitting(BaseStrategy):
    def __init__(self, board):
        super().__init__(board)

    def apply_strategy(self, values, constraints):
        unknowns = Utilities.get_unknown_positions(values)

