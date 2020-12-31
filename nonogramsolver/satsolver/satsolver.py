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
        for application in self._constraint_helper(self.board.get_width(), tuple(constraints)):
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
        for application in self._constraint_helper(self.board.get_height(), tuple(constraints)):
            z3_apps.append(And(*[self.z3_board[i][col] == (a == Board.Cross) for i, a in enumerate(application)]))
        self.solver.add(Or(*z3_apps))
        print('defined col', col)

    def solve(self):
        start_time = time.time()
        print('start crunching')
        res = self.solver.check()
        print('took', time.time() - start_time, 'seconds')
        print(self._constraint_helper.cache_info())
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
    @lru_cache()
    def _constraint_helper(length, constraints):
        if not constraints:
            return [[Board.Empty] * length]
        if sum(constraints) + len(constraints) - 1 > length:
            return [-1]
        c = constraints[0]
        result = []
        apply = [Board.Cross] * c
        new_length = length - c
        if len(constraints) != 1:
            new_length -= 1
            apply += [Board.Empty]
        for app in SatSolver._constraint_helper(new_length, constraints[1:]):
            if app != -1:
                result.append(apply + app)
        apply = [Board.Empty]
        for app in SatSolver._constraint_helper(length - 1, constraints):
            if app != -1:
                result.append(apply + app)
        return result
