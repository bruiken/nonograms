from nonogramsolver.solvingstrategies.basestrategy import BaseStrategy
from nonogramsolver.board import Board


class SimpleBoxes(BaseStrategy):
    """
    Implementation of the simple boxes strategy.
    The idea is that this strategy is the first one called, we fill each row with the constraints from left to right,
    leaving only one space between each constraint. This maximally fills the constraints to the left.
    Then we do the same, but starting from the right (also at the last constraint). If we then find overlap between
    **the same constraints**, those boxes must be filled with crosses.
    """

    def __init__(self, board):
        """
        Constructor for the SimpleBoxes strategy.
        :param board: The board to apply the strategy on.
        """
        super().__init__(board)

    @staticmethod
    def _empty_constraint_application(values, named_constraints):
        """
        Applies the constraints on the value array (which must be empty).
        :param values: The empty (filled with unknown) value array.
        :param named_constraints: List of tuples with the name of the constraint and the constraint itself.
        :return: The filled value array.
        """
        result = [-1 for _ in range(len(values))]
        cur_idx = 0
        for i, constraint in named_constraints:
            if cur_idx > 0:
                cur_idx += 1
            for j in range(cur_idx, cur_idx + constraint):
                result[j] = i
        return result

    @staticmethod
    def _check_overlap(values, values_reversed):
        """
        Checks overlap between the values and the reversed values.
        Values named by -1 are ignored.
        :param values: The values filled from left to right.
        :param values_reversed: The values filled from right to left.
        :return: The new values filled with crosses at overlaps.
        """
        result = []
        for fst, snd in zip(values, values_reversed):
            if fst == snd and fst != -1:
                result.append(Board.Cross)
            else:
                result.append(Board.Unknown)
        return result

    def apply_strategy(self, values, constraints):
        """
        Applies the simple boxes strategy. Note that this strategy can only be applied on an empty board (filled with
        only Unknown values).
        :param values: The values on which we apply the stategy.
        :param constraints: The constraints put on the array of values.
        :return: The new array on which the stategy has been applied.
        """
        if all([v == Board.Unknown for v in values]):
            named_constraints = [(i, c) for i, c in enumerate(constraints)]
            row = SimpleBoxes._empty_constraint_application(values, named_constraints)
            row_reverse = reversed(SimpleBoxes._empty_constraint_application(values, reversed(named_constraints)))
            return SimpleBoxes._check_overlap(row, row_reverse)
        else:
            return values
