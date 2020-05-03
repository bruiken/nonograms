from nonogramsolver.board import BoardReader, PrintBoard
from nonogramsolver.solvingstrategies import SimpleBoxes, SimpleSpaces


if __name__ == '__main__':
    b = BoardReader('exampleboard.json').get_board()
    PrintBoard(b).print()
    SimpleBoxes(b).apply()
    PrintBoard(b).print()
    SimpleSpaces(b).apply()
    PrintBoard(b).print()
