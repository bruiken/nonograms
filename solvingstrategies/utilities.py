from board import Board


class Utilities:
    @staticmethod
    def _get_positions_with_value(values, value):
        val_pos_start = None
        positions = []
        for idx, v in enumerate(values):
            if v == value and val_pos_start is None:
                val_pos_start = idx
            elif val_pos_start is not None and v != value:
                positions.append((val_pos_start, idx - 1))
                val_pos_start = None
        if val_pos_start is not None:
            positions.append((val_pos_start, len(values) - 1))
        return positions

    @staticmethod
    def get_positions_of_scores(values):
        return Utilities._get_positions_with_value(values, Board.Cross)

    @staticmethod
    def get_unknown_positions(values):
        return Utilities._get_positions_with_value(values, Board.Unknown)

    @staticmethod
    def all_blocks_present(values, constraints):
        scores = Board.get_score(values)
        score_positions = Utilities.get_positions_of_scores(values)
        unknown_positions = Utilities.get_unknown_positions(values)
        last_score_end = -999
        if len(scores) == len(constraints):
            for idx, (s_s, s_e) in enumerate(score_positions):
                if Utilities.constraint_fit_in_unknown(constraints[idx], unknown_positions, last_score_end + 1, s_s - 2):
                    if idx < len(scores) - 1:
                        next_constraint = constraints[idx + 1]
                        next_score_dist = score_positions[idx + 1][0] - s_e - 1
                        next_score = scores[idx + 1]
                        curr_score = scores[idx]
                        if Utilities.constraint_fit_in_unknown(next_score_dist, unknown_positions, s_e + 1, score_positions[idx + 1][0] - 1):
                            if next_constraint - curr_score - next_score_dist - next_score == 0:
                                return False
                last_score_end = s_e + 1
            return True
        else:
            return False

    @staticmethod
    def constraint_fit_in_unknown(constraint, unknown_positions, from_idx, to_idx):
        for (u_s, u_e) in unknown_positions:
            if from_idx <= u_s <= to_idx:
                if u_e - u_s + 1 >= constraint and to_idx - from_idx + 1 >= constraint:
                    return True
        return False
