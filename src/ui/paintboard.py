import tkinter as tk
import numpy as np


class PaintBoard(tk.Frame):
    def __init__(self, master=None, picture=None, pixel_size=20, **kwargs):
        super().__init__(master, **kwargs)
        self.pixel_size = pixel_size
        if picture:
            self.grid_size = max(len(picture), len(picture[0]))
        else:
            self.grid_size = 18
        self.default_pixel_color = '#FFFFFF'
        self.default_pixel_rgb = list(self.hex_to_rgb(self.default_pixel_color))
        self.default_grid_color = '#D3D3D3'

        self.pixels = np.zeros([self.grid_size, self.grid_size, 3], dtype=np.uint8)
        # Track whether a grid has color
        self.pixel_ids = [[None for _ in range(self.grid_size)]
                          for _ in range(self.grid_size)]

        self.canvas = tk.Canvas(self,
                                width=self.pixel_size * self.grid_size,
                                height=self.pixel_size * self.grid_size,
                                bg=self.default_pixel_color)
        # self.canvas.bind('<Button-1>', self.handle_click)

        self.draw_grid()

        if picture:
            self.picture = picture
            self.draw_picture()

        self.draw_bold_lines()
        self.canvas.grid(row=0, column=0, sticky='nsew')

    def draw_grid(self):
        for i in range(self.grid_size):
            # Vertical lines
            self.canvas.create_line(i * self.pixel_size, 0, i * self.pixel_size,
                                    self.pixel_size * self.grid_size, fill=self.default_grid_color)
            # Horizontal lines
            self.canvas.create_line(0, i * self.pixel_size, self.pixel_size * self.grid_size,
                                    i * self.pixel_size, fill=self.default_grid_color)

    def draw_bold_lines(self):
        if self.grid_size == 8 or self.grid_size == 10:
            mid_x = self.grid_size * self.pixel_size // 2
            mid_y = self.grid_size * self.pixel_size // 2
            # Vertical line
            self.canvas.create_line(mid_x, 0, mid_x, self.pixel_size * self.grid_size, width=2, fill='#00FF00')
            # Horizontal line
            self.canvas.create_line(0, mid_y, self.pixel_size * self.grid_size, mid_y, width=2, fill='#00FF00')
        elif self.grid_size == 12 or self.grid_size == 15 or self.grid_size == 18:
            cell_width = self.grid_size * self.pixel_size // 3
            cell_height = self.grid_size * self.pixel_size // 3
            # Draw the vertical lines
            self.canvas.create_line(cell_width, 0, cell_width, self.grid_size * self.pixel_size, width=2, fill='#00FF00')
            self.canvas.create_line(2 * cell_width, 0, 2 * cell_width, self.grid_size * self.pixel_size, width=2, fill='#00FF00')

            # Draw the horizontal lines
            self.canvas.create_line(0, cell_height, self.grid_size * self.pixel_size, cell_height, width=2, fill='#00FF00')
            self.canvas.create_line(0, 2 * cell_height, self.grid_size * self.pixel_size, 2 * cell_height, width=2, fill='#00FF00')

    def draw_picture(self):
        for x in range(len(self.picture)):
            for y in range(len(self.picture[x])):
                if self.picture[x][y]:
                    self.pixels[y, x] = list(self.hex_to_rgb('#000000'))
                    self.paint_pixel(y, x)

    def handle_click(self, event=None):
        # Calculate the pixel location based on click coordinates
        col = event.x // self.pixel_size
        row = event.y // self.pixel_size
        print(col, row)
        if 0 <= col < self.grid_size and 0 <= row < self.grid_size:
            self.pixels[row, col] = self.default_pixel_rgb

            # Draw or update only the clicked pixel
            self.paint_pixel(row, col)

    def paint_pixel(self, row, col):
        x1 = col * self.pixel_size
        y1 = row * self.pixel_size
        x2 = x1 + self.pixel_size
        y2 = y1 + self.pixel_size
        color = self.rgb_to_hex(self.pixels[row, col])

        # If a pixel is already drawn, delete it before creating a new one
        if self.pixel_ids[row][col] is not None:
            # print(f'deleted {self.pixel_ids[row][col]}')
            self.canvas.delete(self.pixel_ids[row][col])
        # Draw the rectangle (pixel) and store its ID for future reference
        self.pixel_ids[row][col] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
        # print(f'drew {self.pixel_ids[row][col]}')

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


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Nonogram!')
    paintboard = PaintBoard(root)
    root.mainloop()
