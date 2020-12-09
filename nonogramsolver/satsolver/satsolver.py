from z3 import *

from nonogramsolver.board import Board
from collections.abc import Iterable
import time
from functools import lru_cache


def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            if not isinstance(el[0], Iterable):  # noqa
                yield el
            else:
                yield from flatten(el)
        else:
            yield el


class SatSolver:
    def __init__(self, board):
        self.board = board
        self.solver = Solver()
        self.z3_board = self.create_board()
        self.z3_col_constraints = self.create_col_constraints()
        self.z3_row_constraints = self.create_row_constraints()
        self.define_row_constraints()
        self.define_col_constraints()

    def create_board(self):
        res = []
        for i in range(self.board.get_height()):
            temp_row = []
            for j in range(self.board.get_width()):
                temp_row.append(Bool('field_{}_{}'.format(i, j)))
            res.append(temp_row)
        return res

    def create_col_constraints(self):
        res = []
        for col, constraints in enumerate(self.board.get_col_constraints()):
            constraint_vector = IntVector('col_{}'.format(col), len(constraints))
            res.append(constraint_vector)
            for i, constraint in enumerate(constraints):
                self.solver.add(constraint_vector[i] == constraint)
        return res

    def create_row_constraints(self):
        res = []
        for row, constraints in enumerate(self.board.get_row_constraints()):
            constraint_vector = IntVector('row_{}'.format(row), len(constraints))
            res.append(constraint_vector)
            for i, constraint in enumerate(constraints):
                self.solver.add(constraint_vector[i] == constraint)
        return res

    def define_row_constraints(self):
        for i in range(self.board.get_height()):
            self.define_row_constraint(i)

    def define_row_constraint(self, row):
        if not self.board.get_row_constraints()[row]:
            self.define_empty_row_constraint(row)
        else:
            self.define_non_empty_row_constraint(row)

    def define_empty_row_constraint(self, row):
        for val in self.z3_board[row]:
            self.solver.add(val == False)  # noqa

    def define_non_empty_row_constraint(self, row):
        constraints = self.board.get_row_constraints()[row]
        z3_apps = []
        for application in self._get_possible_constraint_applications(constraints, self.board.get_width()):
            z3_apps.append(And(*[self.z3_board[row][i] == (a == Board.Cross) for i, a in enumerate(application)]))
        self.solver.add(Or(*z3_apps))
        print('defined row', row)

    def define_col_constraints(self):
        for i in range(self.board.get_width()):
            self.define_col_constraint(i)

    def define_col_constraint(self, col):
        if not self.board.get_col_constraints()[col]:
            self.define_empty_col_constraint(col)
        else:
            self.define_non_empty_col_constraint(col)

    def define_empty_col_constraint(self, col):
        for val in [row[col] for row in self.z3_board]:
            self.solver.add(val == False)  # noqa

    def define_non_empty_col_constraint(self, col):
        constraints = self.board.get_col_constraints()[col]
        z3_apps = []
        for application in self._get_possible_constraint_applications(constraints, self.board.get_height()):
            z3_apps.append(And(*[self.z3_board[i][col] == (a == Board.Cross) for i, a in enumerate(application)]))
        self.solver.add(Or(*z3_apps))
        print('defined col', col)

    def solve(self):
        start_time = time.time()
        print('start crunching')
        res = self.solver.check()
        print('took', time.time() - start_time, 'seconds')
        if res == sat:
            self.apply_result(self.solver.model())
            return True
        return False

    def apply_result(self, model):
        for col in range(self.board.get_width()):
            for row in range(self.board.get_height()):
                self.board.set_position(
                    col, row,
                    Board.Cross if is_true(model[self.z3_board[row][col]]) else Board.Empty
                )

    @staticmethod
    def _get_possible_constraint_applications(constraints, max_length):
        res = SatSolver._constraint_helpers(constraints, [], 0, max_length)
        return flatten(res)

    @staticmethod
    def _constraint_helpers(constraints_left, current_values, index, max_length):
        if len(current_values) > max_length:
            return []
        if not constraints_left:
            current_values += [Board.Empty] * (max_length - len(current_values))
            return current_values
        if len(current_values) + sum(constraints_left) + len(constraints_left) - 2 > max_length:
            return []
        result = []
        no_application = SatSolver._constraint_helpers(constraints_left,
                                                       list(current_values) + [Board.Empty],
                                                       index + 1,
                                                       max_length)
        if no_application:
            result.append(no_application)

        new_values = current_values + [Board.Cross] * constraints_left[0] + ([] if len(constraints_left) == 1 else [Board.Empty])
        application = SatSolver._constraint_helpers(constraints_left[1:],
                                                    new_values,
                                                    index + len(new_values) - len(current_values),
                                                    max_length)
        if application:
            result.append(application)
        return result
