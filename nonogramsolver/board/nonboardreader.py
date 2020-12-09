from nonogramsolver.board.board import Board


class NonBoardReader:
    """
    Reads a nonogram in the .non format.
    """

    def __init__(self, path):
        """
        Constructor for a NonBoardReader.
        :param path: The path to the .non file.
        """
        self.path = path

    def _get_board_data(self):
        """
        Gets the board data from the given file.
        :return: a list of all the board file lines.
        """
        with open(self.path, 'r') as f:
            return f.readlines()

    def get_board(self):
        """
        Get a Board instance that represents the board in the given file.
        :return: The Board of the file.
        """
        data = self._get_board_data()
        width, height = 0, 0
        row_constraints, col_constraints = [], []
        reading_col_constraint, reading_row_constraint = False, False
        for line in data:
            line = line.strip('\n')
            if line.startswith('width'):
                width = int(line.split()[1])
                continue
            if line.startswith('height'):
                height = int(line.split()[1])
                continue
            if line.startswith('rows'):
                reading_row_constraint = True
                continue
            if line.startswith('columns'):
                reading_col_constraint = True
                continue
            if not line:
                reading_row_constraint = False
                reading_col_constraint = False
                continue
            if reading_row_constraint:
                row_constraints.append([int(x) for x in line.split(',')])
                continue
            if reading_col_constraint:
                col_constraints.append([int(x) for x in line.split(',')])
                continue
        return Board(width, height, row_constraints, col_constraints)
