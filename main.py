from nonogramsolver.board import PrintBoard, NonBoardReader
from nonogramsolver.satsolver import SatSolver


if __name__ == '__main__':
    b2 = NonBoardReader('examples/529.non').get_board()
    print(b2.get_height(), b2.get_width(), b2.get_col_constraints())
    PrintBoard(b2).print()
    solver = SatSolver(b2)
    solver.solve()
    PrintBoard(b2).print()
