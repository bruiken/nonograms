from nonogramsolver.solvingstrategies.basestrategy import BaseStrategy
from nonogramsolver.board import Board
from nonogramsolver.solvingstrategies.utilities import Utilities


class SimpleSpaces(BaseStrategy):
    def __init__(self, board):
        super().__init__(board)

    def apply_strategy(self, values, constraints):
        scores = self.board.get_score(values)
        new_vals = list(values)
        if Utilities.all_blocks_present(values, constraints):
            taken_spots = [v != Board.Unknown for v in values]
            diffs = [c - s for s, c in zip(scores, constraints)]
            score_positions = Utilities.get_positions_of_scores(values)
            for diff, (s_s, s_e) in zip(diffs, score_positions):
                for p in range(max(0, s_s - diff), min(len(values), s_e + 1 + diff)):
                    taken_spots[p] = True
            for idx, t in enumerate(taken_spots):
                if not t:
                    new_vals[idx] = Board.Empty
        return new_vals
