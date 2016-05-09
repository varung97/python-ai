"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

#testing
import poc_fifteen_gui
LR_DICT = {
           -1: "l",
           1: "r"
          }

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self.get_number(target_row, target_col) != 0:
            return False

        for row_idx in range(target_row + 1, self.get_height()):
            for col_idx in range(self.get_width() - 1):
                expected_pos = self.current_position(row_idx, col_idx)
                if row_idx != expected_pos[0] or col_idx != expected_pos[1]:
                    return False

        for col_idx in range(target_col + 1, self.get_width()):
            expected_pos = self.current_position(target_row, col_idx)
            if target_row != expected_pos[0] or col_idx != expected_pos[1]:
                return False

        return True

    def position_tile(self, target_row, target_col, actual_tile_pos):
        """
        Moves tile at actual_tile_pos to (target_row, target_col)
        with the 0 to the left of it
        """
        move_string = ""

        horiz_offset = actual_tile_pos[1] - target_col

        if horiz_offset != 0:
            left_or_right = horiz_offset/abs(horiz_offset)
            # using LR_DICT, it can be determined from
            # left_or_right whether 0 has to travel to
            # left or to right

            if actual_tile_pos[0] == 0:
                # This sequence moves the required tile
                # one row down so that the row above it
                # is free for subsequent moves
                move_string += "u" * (target_row - 1)
                move_string += LR_DICT[left_or_right] * abs(horiz_offset)
                move_string += "u"
                move_string += LR_DICT[left_or_right * -1] + "d"
                actual_tile_pos = (actual_tile_pos[0] + 1, actual_tile_pos[1])
                # 0 tile is positioned to l/r of target
                # tile
            else:
                move_string += "u" * (target_row - actual_tile_pos[0])
                move_string += LR_DICT[left_or_right] * (abs(horiz_offset) - 1)

            move_string += LR_DICT[left_or_right]
            # Moves tile horizontally once

            for dummy_var in range(abs(horiz_offset) - 1):
                # Moves tile horizontally until it lies
                # vertically above target position
                move_string += "u" + 2 * LR_DICT[left_or_right * -1] + "d" + LR_DICT[left_or_right]

            if horiz_offset > 0:
                move_string += "ulld"

            if actual_tile_pos[0] < target_row:
                move_string += "dru"
            else:
                move_string += "ur"
        else:
            move_string += "u" * (target_row - actual_tile_pos[0])

        if actual_tile_pos[0] < target_row:
            actual_tile_pos = (actual_tile_pos[0] + 1, actual_tile_pos[1])

        # at the end of this sequence, tile is
        # vertically above target position and has
        # moved one or two positions down depending upon
        # where it started from

        for dummy_var in range(target_row - actual_tile_pos[0]):
            move_string += "lddru"

        return move_string + "ld"

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col)

        move_string = ""

        original_tile_pos = self.current_position(target_row, target_col)
        move_string += self.position_tile(target_row, target_col, original_tile_pos)

        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row, target_col - 1)
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0)

        move_string = "ur"
        original_tile_pos = self.current_position(target_row, 0)

        if original_tile_pos[0] != target_row - 1 or original_tile_pos[1] != 0:
            if original_tile_pos[0] == target_row - 1 and original_tile_pos[1] == 1:
                original_tile_pos = (target_row - 1, 0)

            move_string += self.position_tile(target_row - 1, 1, original_tile_pos)
            move_string += "rrdllurdru"
            move_string += "r" * (self.get_width() - 3)
        else:
            move_string += "r" * (self.get_width() - 2)

        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)
        return move_string

    #############################################################
    # Phase two methods

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(1, target_col) != 0:
            return False

        for row_idx in range(2, self.get_height()):
            for col_idx in range(self.get_width() - 1):
                expected_pos = self.current_position(row_idx, col_idx)
                if row_idx != expected_pos[0] or col_idx != expected_pos[1]:
                    return False

        for row_idx in range(2):
            for col_idx in range(target_col + 1, self.get_width()):
                expected_pos = self.current_position(row_idx, col_idx)
                if row_idx != expected_pos[0] or col_idx != expected_pos[1]:
                    return False

        return True

    def solve_col_top(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)

        move_string = ""

        row0_tile_pos = self.current_position(0, target_col)
        row1_tile_pos = self.current_position(1, target_col)

        if ((row0_tile_pos == (1, target_col - 1) and row1_tile_pos == (0, target_col)) or
            (row0_tile_pos == (0, target_col) and row1_tile_pos == (0, target_col - 1)) or
            (row1_tile_pos == (1, target_col - 1) and row1_tile_pos != (0, target_col))
           ):
            move_string += self.position_tile(1, target_col, row1_tile_pos)

            row0_tile_pos = self.current_position(0, target_col)
            move_string += self.position_tile(1, target_col - 1, row0_tile_pos)
            move_string += "urdlurrdluldrruld"
            self.update_puzzle(move_string)
        else:
            move_string += self.position_tile(1, target_col, row0_tile_pos)
            self.update_puzzle(move_string)

            row1_tile_pos = self.current_position(1, target_col)

            rem_move_string = self.position_tile(1, target_col - 1, row1_tile_pos)
            rem_move_string += "urrdl"
            self.update_puzzle(rem_move_string)
            move_string += rem_move_string

        assert self.row1_invariant(target_col - 1)
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1)

        move_string = "ul"
        self.update_puzzle(move_string)

        if self.current_position(0, 1) == (1, 1):
            move_string += "rdlu"
            self.update_puzzle("rdul")
        elif self.current_position(0, 1) == (1, 0):
            move_string += "drul"
            self.update_puzzle("drul")

        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ""
        pos_of_0 = self.current_position(0, 0)

        horiz_offset = self.get_width() - 1 - pos_of_0[1]
        move_string += "r" * horiz_offset

        vert_offset = self.get_height() - 1 - pos_of_0[0]
        move_string += "d" * vert_offset

        self.update_puzzle(move_string)

        for row in range(self.get_height() - 1, 1, -1):
            for col in range(self.get_width() - 1, 0, -1):
                move_string += self.solve_interior_tile(row, col)
            move_string += self.solve_col0_tile(row)

        for col in range(self.get_width() - 1, 1, -1):
            move_string += self.solve_col_top(col)

        move_string += self.solve_2x2()

        while ("ud" in move_string or
               "du" in move_string or
               "lr" in move_string or
               "rl" in move_string):
            move_string = move_string.replace("ud", "")
            move_string = move_string.replace("du", "")
            move_string = move_string.replace("lr", "")
            move_string = move_string.replace("rl", "")

        return move_string


# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, [[15, 11, 8, 12], [14, 10, 9, 13], [2, 6, 1, 4], [3, 7, 5, 0]]))
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

puzzle = Puzzle(4, 4, [[15, 11, 8, 12], [14, 10, 9, 13], [2, 6, 1, 4], [3, 7, 5, 0]])
sol = puzzle.solve_puzzle()
print sol
print len(sol)
