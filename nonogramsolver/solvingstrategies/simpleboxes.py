from nonogramsolver.solvingstrategies.basestrategy import BaseStrategy
from nonogramsolver.board import Board


class SimpleBoxes(BaseStrategy):
    def __init__(self, board):
        super().__init__(board)

    @staticmethod
    def _empty_constraint_application(values, constraints):
        result = [-1 for _ in range(len(values))]
        cur_idx = 0
        for i, constraint in enumerate(constraints):
            if cur_idx > 0:
                cur_idx += 1
            for j in range(cur_idx, cur_idx + constraint):
                result[j] = i
        return result

    @staticmethod
    def _check_overlap(values, values_reversed):
        result = []
        for fst, snd in zip(values, values_reversed):
            if fst == snd and fst != -1:
                result.append(Board.Cross)
            else:
                result.append(Board.Unknown)
        return result

    def apply_strategy(self, values, constraints):
        if all([v == Board.Unknown for v in values]):
            row = SimpleBoxes._empty_constraint_application(values, constraints)
            row_reverse = reversed(SimpleBoxes._empty_constraint_application(values, reversed(constraints)))
            return SimpleBoxes._check_overlap(row, row_reverse)
        else:
            return values
