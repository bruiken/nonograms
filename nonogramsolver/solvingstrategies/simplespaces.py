from nonogramsolver.solvingstrategies.basestrategy import BaseStrategy
from nonogramsolver.board import Board
from nonogramsolver.solvingstrategies.utilities import Utilities


class SimpleSpaces(BaseStrategy):
    """
    Simplespaces is a strategy that can be applied when we are sure that all of the constraint blocks are in the
    array already.
    The idea is to find the spots that must be empty, we can do this by extending the score blocks to the left and right
    in the array upto the constraint it represents. This identifies the possible positions the score block can extend
    to. After we have done this for every score block, we can find the spots that are impossible to be filled with
    crosses. Those spots can be set to empty.
    """

    def __init__(self, board):
        """
        Constructor for the SimpleSpaces strategy.
        :param board: The board to apply the strategy on.
        """
        super().__init__(board)

    def apply_strategy(self, values, constraints):
        """
        Applies the simple spaces strategy.
        :param values: The array of values.
        :param constraints: the constraints put on the values.
        :return: The new values after the application of the algorithm.
        """
        scores = self.board.get_score(values)
        new_vals = list(values)
        if Utilities.all_blocks_present(values, constraints):  # only apply when all blocks are present
            taken_spots = [v != Board.Unknown for v in values]  # array to keep track of which spots are taken
            diffs = [c - s for s, c in zip(scores, constraints)]  # array to see how far each score still has to go
            score_positions = Utilities.get_positions_of_scores(values)
            for diff, (s_s, s_e) in zip(diffs, score_positions):
                for p in range(max(0, s_s - diff), min(len(values), s_e + 1 + diff)):
                    taken_spots[p] = True  # set each possible spot where a cross could go to True
            for idx, t in enumerate(taken_spots):  # calculate the result
                if not t:
                    new_vals[idx] = Board.Empty
        return new_vals
