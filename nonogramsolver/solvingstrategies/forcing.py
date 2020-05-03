from nonogramsolver.solvingstrategies.basestrategy import BaseStrategy
from nonogramsolver.solvingstrategies.utilities import Utilities


class Forcing(BaseStrategy):
    def __init__(self, board):
        super().__init__(board)

    def apply_strategy(self, values, constraints):
        score_positions = Utilities.get_positions_of_scores(values)
        unknown_positions = Utilities.get_unknown_positions(values)
        # fill from left to right:
        #   fill unknown position with as many constraints as possible
        #   also keep track of score positions to account for blocks that are already created
        # then do the same from right to left
        # if all the constraints are put in the same blocks ltr and rtl then you which constraints are in the blocks
        cur_score_pos = score_positions.pop(0) if score_positions else None
        cur_unknown_pos = unknown_positions.pop(0) if unknown_positions else None

