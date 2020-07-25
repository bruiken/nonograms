from nonogramsolver.board import BoardReader, PrintBoard
from nonogramsolver.solvingstrategies import SimpleBoxes

if __name__ == '__main__':
    b = BoardReader('examples/exampleboard.json').get_board()
    PrintBoard(b).print()
    SimpleBoxes(b).apply()
    PrintBoard(b).print()
