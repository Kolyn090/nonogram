from cellstate import CellState
from solveresult import SolverResult
from util.bitarray import BitArray
from solution import Solution
import copy


class Solver:
    def __init__(self, descr):
        self.width = descr.width
        self.height = descr.height
        self.cells = []
        self.descr = descr
        self.solve_result = SolverResult.NOT_ATTEMPTED

        self.cur_row = []
        self.cur_row_length = 0
        self.cur_row_bits = None
        self.cur_row_filled = None
        self.cur_row_not_empty = None
        self.cur_description = None
        self.cur_row_impossible = False

        self.verbose = True
        self.counter_example = None

        for i in range(self.width):
            self.cells.append([CellState.NOT_DECIDED] * self.height)

    def solve_row(self, row, descr):
        if self.verbose:
            sb = 'Solving row: '
            sb += ' '.join([str(num) for num in descr])
            sb += '\t'
            # for cs in row:
            #     print(str(cs.value))
            sb += ''.join([str(cs.value) for cs in row])
            print(sb)

        self.cur_row = row
        self.cur_description = descr
        self.cur_row_length = len(self.cur_row)
        self.cur_row_bits = BitArray(self.cur_row_length)
        self.cur_row_filled = BitArray(self.cur_row_length)  # True
        self.cur_row_not_empty = BitArray(self.cur_row_length)  # False
        self.cur_description = descr

        for i in range(self.cur_row_length):
            self.cur_row_filled.set_bit(i, True)

        if not self.solve_row_rec(0, 0):
            self.cur_row_impossible = True
            return False

        changed = False
        for x in range(self.cur_row_length):
            if self.cur_row[x] == CellState.NOT_DECIDED:
                if self.cur_row_filled.get_bit(x):
                    self.cur_row[x] = CellState.FILLED
                    changed = True
                elif not self.cur_row_not_empty.get_bit(x):
                    self.cur_row[x] = CellState.EMPTY
                    changed = True

        if changed and self.verbose:
            sb = 'Changed to: '
            sb += ''.join([str(cs.value) for cs in self.cur_row])
            print(sb)

        return False

    def solve_row_rec(self, pos, nums_used):
        if nums_used == len(self.cur_description):
            assert pos <= self.cur_row_length
            for x in range(pos, self.cur_row_length):
                if self.cur_row[x] == CellState.FILLED:
                    return False
            self.cur_row_filled.and_with(self.cur_row_bits)
            self.cur_row_not_empty.or_with(self.cur_row_bits)
            return True

        cur_len = self.cur_description[nums_used]

        # Go through all possible starts
        feasible = False
        for x in range(pos, self.cur_row_length):
            if x + cur_len > self.cur_row_length:
                break

            can_be_filled = True
            for i in range(x, x + cur_len):
                if self.cur_row[i] == CellState.EMPTY:
                    can_be_filled = False
                    break

            if (can_be_filled and
                    x + cur_len < self.cur_row_length and
                    self.cur_row[x + cur_len] == CellState.FILLED):
                can_be_filled = False

            if can_be_filled:
                for i in range(x, x + cur_len):
                    self.cur_row_bits.set_bit(i, True)
                empty_cell = 0 if x + cur_len == self.cur_row_length else 1
                if self.solve_row_rec(x + cur_len + empty_cell, nums_used + 1):
                    feasible = True
                for i in range(x, x + cur_len):
                    self.cur_row_bits.set_bit(i, False)

            if self.cur_row[x] == CellState.FILLED:
                break

        return feasible

    def solve_step(self):
        def remove_zero_from_list(lst):
            return [item for item in lst if item != 0]

        changed = False
        # Check all columns
        for x in range(self.width):
            col = self.cells[x]
            if self.solve_row(col, remove_zero_from_list(self.descr.get_col_description(x))):
                changed = True
                for y in range(self.height):
                    self.cells[x][y] = col[y]
            if self.cur_row_impossible:
                return False

        # Check all rows
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(self.cells[x][y])

            if self.solve_row(row, remove_zero_from_list(self.descr.get_row_description(y))):
                changed = True
                for x in range(self.width):
                    self.cells[x][y] = row[x]
            if self.cur_row_impossible:
                return False

        return changed

    def solve_rec(self):
        self.cur_row_impossible = False
        while True:
            changed = self.solve_step()
            if self.cur_row_impossible:
                return SolverResult.IMPOSSIBLE
            if not changed:
                break

        solved = True
        bad_x, bad_y = 0, 0
        for x in range(self.width):
            for y in range(self.height):
                if self.cells[x][y] == CellState.NOT_DECIDED:
                    solved = False
                    bad_x = x
                    bad_y = y
                    break

        if solved:
            return SolverResult.SOLVED

        # Go deeper
        backup_cells = self.clone_cells()
        self.cells[bad_x][bad_y] = CellState.EMPTY
        if self.solve_rec() == SolverResult.SOLVED:
            return SolverResult.SOLVED
        else:
            self.cells = backup_cells
            self.cells[bad_x][bad_y] = CellState.FILLED
            return self.solve_rec()

    def solve(self):
        if self.solve_rec() == SolverResult.IMPOSSIBLE:
            self.solve_result = SolverResult.IMPOSSIBLE
            return None
        else:
            self.solve_result = SolverResult.SOLVED
            return Solution(self.cells)

    def clone_cells(self):
        return copy.deepcopy(self.cells)

    def flip_state(self, x):
        if x == CellState.FILLED:
            return CellState.EMPTY
        elif x == CellState.EMPTY:
            return CellState.FILLED
        else:
            return x
