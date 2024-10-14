import tkinter as tk
import numpy as np
from matrix_observer import Matrix_Observer


class PaintBoard(tk.Frame, Matrix_Observer):
    def __init__(self, master=None, picture=None, pixel_size=20, **kwargs):
        super().__init__(master, **kwargs)
        self.pixel_size = pixel_size
        if picture:
            self.grid_width = len(picture)
            self.grid_height = len(picture[0])
        else:
            self.grid_width = 10
            self.grid_height = 10

        self.default_pixel_color = '#FFFFFF'
        self.default_pixel_rgb = list(self.hex_to_rgb(self.default_pixel_color))
        self.default_grid_color = '#D3D3D3'

        self.pixels = np.zeros([self.grid_width, self.grid_height, 3], dtype=np.uint8)
        # Track whether a grid has color
        self.pixel_ids = [[None for _ in range(self.grid_width)]
                          for _ in range(self.grid_height)]

        self.canvas = tk.Canvas(self,
                                width=self.pixel_size * self.grid_width,
                                height=self.pixel_size * self.grid_height,
                                bg=self.default_pixel_color)

        self.draw_grid()

        if picture:
            self.picture = picture
            self.draw_picture()

        self.draw_bold_lines()
        self.canvas.grid(row=0, column=0, sticky='nsew')

    def draw_grid(self):
        # Draw the grid lines for a rectangular grid
        for i in range(self.grid_width):
            # Vertical lines
            self.canvas.create_line(
                i * self.pixel_size, 0,
                i * self.pixel_size, self.pixel_size * self.grid_height,
                fill=self.default_grid_color
            )

        for j in range(self.grid_height):
            # Horizontal lines
            self.canvas.create_line(
                0, j * self.pixel_size,
                self.pixel_size * self.grid_width, j * self.pixel_size,
                fill=self.default_grid_color
            )

    def draw_bold_lines(self):
        if self.grid_width in [8, 10]:
            mid_x = self.grid_width * self.pixel_size // 2
            # Vertical line through the middle
            self.canvas.create_line(mid_x, 0, mid_x, self.pixel_size * self.grid_height, width=2, fill='#00FF00')

        elif self.grid_width in [12, 15, 18]:
            cell_width = self.grid_width * self.pixel_size // 3
            # Draw the vertical lines at 1/3 and 2/3 of the width
            self.canvas.create_line(cell_width, 0, cell_width, self.pixel_size * self.grid_height, width=2,
                                    fill='#00FF00')
            self.canvas.create_line(2 * cell_width, 0, 2 * cell_width, self.pixel_size * self.grid_height, width=2,
                                    fill='#00FF00')
        elif self.grid_width in [20]:
            cell_width = self.grid_width * self.pixel_size // 4
            # Draw the vertical lines at 1/4 and 2/4 and 3/4 of the width
            self.canvas.create_line(cell_width, 0, cell_width, self.pixel_size * self.grid_height, width=2,
                                    fill='#00FF00')
            self.canvas.create_line(2 * cell_width, 0, 2 * cell_width, self.pixel_size * self.grid_height, width=2,
                                    fill='#00FF00')
            self.canvas.create_line(3 * cell_width, 0, 3 * cell_width, self.pixel_size * self.grid_height, width=2,
                                    fill='#00FF00')

        if self.grid_height in [8, 10]:
            mid_y = self.grid_height * self.pixel_size // 2
            # Horizontal line through the middle
            self.canvas.create_line(0, mid_y, self.pixel_size * self.grid_width, mid_y, width=2, fill='#00FF00')
        elif self.grid_height in [12, 15, 18]:
            cell_height = self.grid_height * self.pixel_size // 3
            # Draw the horizontal lines at 1/3 and 2/3 of the height
            self.canvas.create_line(0, cell_height, self.pixel_size * self.grid_width, cell_height, width=2,
                                    fill='#00FF00')
            self.canvas.create_line(0, 2 * cell_height, self.pixel_size * self.grid_width, 2 * cell_height, width=2,
                                    fill='#00FF00')
        elif self.grid_height in [20]:
            cell_height = self.grid_height * self.pixel_size // 4
            # Draw the horizontal lines at 1/4 and 2/4 and 3/4 of the height
            self.canvas.create_line(0, cell_height, self.pixel_size * self.grid_width, cell_height, width=2,
                                    fill='#00FF00')
            self.canvas.create_line(0, 2 * cell_height, self.pixel_size * self.grid_width, 2 * cell_height, width=2,
                                    fill='#00FF00')
            self.canvas.create_line(0, 3 * cell_height, self.pixel_size * self.grid_width, 3 * cell_height, width=2,
                                    fill='#00FF00')

    def paint_pixel(self, row, col):
        x1 = row * self.pixel_size
        y1 = col * self.pixel_size
        x2 = x1 + self.pixel_size
        y2 = y1 + self.pixel_size
        color = self.rgb_to_hex(self.pixels[row][col])

        # If a pixel is already drawn, delete it before creating a new one
        if self.pixel_ids[row][col] is not None:
            self.canvas.delete(self.pixel_ids[row][col])
        # Draw the rectangle (pixel) and store its ID for future reference
        self.pixel_ids[row][col] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

    def draw_picture(self):
        for x in range(len(self.picture)):
            for y in range(len(self.picture[x])):
                if self.picture[x][y]:
                    self.pixels[x][y] = list(self.hex_to_rgb('#000000'))
                    self.paint_pixel(x, y)

    def hex_to_rgb(self, hexcode):
        # Remove the hash (#) if it exists
        hexcode = hexcode.lstrip('#')

        # Convert the hex code into an RGB tuple
        if len(hexcode) == 6:
            # Each pair of hex digits corresponds to an RGB component
            return tuple(int(hexcode[i:i + 2], 16) for i in (0, 2, 4))
        elif len(hexcode) == 3:
            # For shorthand hex codes like #FFF, double each digit
            return tuple(int(hexcode[i] * 2, 16) for i in range(3))
        else:
            raise ValueError("Hexcode must be in the format #RRGGBB or #RGB")

    def rgb_to_hex(self, rgb_lst):
        # Convert each component to a two-character hex string and join them
        return '#{:02X}{:02X}{:02X}'.format(*list(rgb_lst))

    def adjust_size(self, width, height):
        self.grid_width = width
        self.grid_height = height

        self.pixels = np.zeros([self.grid_width, self.grid_height, 3], dtype=np.uint8)
        # Track whether a grid has color
        self.pixel_ids = [[None for _ in range(self.grid_height)]
                          for _ in range(self.grid_width)]

        self.canvas.destroy()
        self.canvas = tk.Canvas(self,
                                width=self.pixel_size * self.grid_width,
                                height=self.pixel_size * self.grid_height,
                                bg=self.default_pixel_color)
        self.draw_grid()

        self.draw_bold_lines()
        self.canvas.grid(row=0, column=0, sticky='nsew')

    def render_picture(self, picture):
        if picture:
            self.picture = picture
            self.update_row(len(picture))
            self.update_column(len(picture[0]))
            self.draw_picture()
            self.draw_bold_lines()

    def update_row(self, newlen):
        self.adjust_size(newlen, self.grid_height)

    def update_column(self, newlen):
        self.adjust_size(self.grid_width, newlen)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Nonogram!')
    paintboard = PaintBoard(root)
    paintboard.pack()
    root.mainloop()
