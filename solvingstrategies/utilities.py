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

