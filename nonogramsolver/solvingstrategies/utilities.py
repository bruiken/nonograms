from nonogramsolver.board import Board


class Utilities:
    """
    Various utility functions used in the solving strategies.
    """

    @staticmethod
    def _get_positions_with_value(values, value):
        """
        Function to get all the positions with the given value in a list of
        values.
        :param values: The List of values to look in.
        :param value: The value to look for.
        :return: A list of tuples that contain the start- and end-indices of
                 the blocks.
        """
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
        """
        Get all the positions in the given array where the crosses are.
        :param values: The array of values.
        :return: A list of tuples that contain the start- and end-indices of
                 the blocks.
        """
        return Utilities._get_positions_with_value(values, Board.Cross)

    @staticmethod
    def get_unknown_positions(values):
        """
        Get all the positions in the given array where the unknown positions
        are.
        :param values: The array of values.
        :return: A list of tuples that contain the start- and end-indices of
                 the blocks.
        """
        return Utilities._get_positions_with_value(values, Board.Unknown)

    @staticmethod
    def all_blocks_present(values, constraints):
        """
        Check if we definitely know that all the separate blocks are there
        already.
        :param values: The array of values.
        :param constraints: The constraints put on the array of values.
        :return: True if all the blocks of scores are present, False if not or
                 if we cannot know.
        """
        scores = Board.get_score(values)
        if scores == constraints:  # case where the scores are all done already
            return True
        if len(scores) == len(constraints):
            return not Utilities._blocks_may_join(values, scores, constraints)
        return False

    @staticmethod
    def _blocks_may_join(values, scores, constraints):
        """
        Checks if existing blocks of crosses may join in an array of values.
        :param values: The array of values to check.
        :param scores: The scores of the values.
        :param constraints: The constraints put on the values.
        :return: True if it may be the case that two blocks are going to join,
                 False otherwise.
        """
        last_score_end = -999  # large negative integer for a minimum index
        score_pos = Utilities.get_positions_of_scores(values)
        unknown_pos = Utilities.get_unknown_positions(values)
        for idx, (s_s, s_e) in enumerate(score_pos):
            if Utilities.constraint_fit_in_unknown(constraints[idx],
                                                   unknown_pos,
                                                   last_score_end + 1,
                                                   s_s - 2) and \
                idx < len(scores) - 1 and \
                    Utilities._block_may_join(constraints[idx + 1],
                                              score_pos[idx + 1][0], s_e,
                                              scores[idx], scores[idx + 1],
                                              unknown_pos):
                return True
            last_score_end = s_e + 1
        return False

    @staticmethod
    def _block_may_join(next_constraint, start_next_score, end_current_score,
                        current_score, next_score, unknowns):
        """
        Checks if a block may join with another one. We do this by comparing
        the current score/block to the next one.
        :param next_constraint: The constraint put on the next block.
        :param start_next_score: The start index of the next block.
        :param end_current_score: The end index of the current block.
        :param current_score: The score of the current block.
        :param next_score: The score of the next block.
        :param unknowns: A list of pairs indicating the positions of unknown
                         blocks.
        :return: True if the two blocks may join, False otherwise.
        """
        next_score_dist = start_next_score - end_current_score - 1
        if Utilities.constraint_fit_in_unknown(next_score_dist, unknowns,
                                               end_current_score + 1,
                                               start_next_score - 1):
            check = next_constraint - current_score - \
                next_score_dist - next_score
            if check == 0:
                return True
        return False

    @staticmethod
    def constraint_fit_in_unknown(constraint, unknown_positions, from_idx,
                                  to_idx):
        """
        Checks if a constraint may fit in unknown values based on a start- and
        end-index.
        :param constraint: The constraint we want to fit.
        :param unknown_positions: The list of pairs indicating the unknown
                                  positions.
        :param from_idx: The start index to look for.
        :param to_idx: The end index to look for.
        :return: True if the constraint can fit inside a block of unknown
                 values.
        """
        for (u_s, u_e) in unknown_positions:
            if from_idx <= u_s <= to_idx and \
                    u_e - u_s + 1 >= constraint and \
                    to_idx - from_idx + 1 >= constraint:
                return True
        return False
