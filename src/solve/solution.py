from cellstate import CellState


class Solution:
    def __init__(self, cells):
        self.EMPTY_MARKER = '☐'
        self.FILL_MARKER = '☒'
        self.width = len(cells)
        self.height = len(cells[0])
        self.pixels = []
        for x in range(self.width):
            self.pixels.append([False] * self.height)
            for y in range(self.height):
                self.pixels[x][y] = cells[x][y] == CellState.FILLED

    def __str__(self):
        sb = ''
        for y in range(self.height):
            for x in range(self.width):
                sb += self.FILL_MARKER if self.pixels[x][y] else self.EMPTY_MARKER
            if y != self.height - 1:
                sb += '\n'
        return sb
