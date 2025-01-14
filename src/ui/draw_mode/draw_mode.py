import cv2
import numpy as np


class Draw_Mode:
    def __init__(self, paintboard):
        self.paintboard = paintboard
        self.pixel_size = paintboard.pixel_size
        self._draw_mode = False

    def handle_click(self, event=None):
        if not self._draw_mode:
            return

        # Calculate the pixel location based on click coordinates
        row = event.x // self.pixel_size
        col = event.y // self.pixel_size
        if 0 <= row < self.paintboard.grid_width and 0 <= col < self.paintboard.grid_height:
            curr_pixel = self.paintboard.pixels[row, col]
            if np.array_equal(curr_pixel, self.paintboard.paint_rgb):
                self.paintboard.pixels[row][col] = self.paintboard.default_pixel_rgb
            else:
                self.paintboard.pixels[row][col] = self.paintboard.paint_rgb
            self.paintboard.paint_pixel(row, col)

    def get_binary_image(self):
        def make_binary(cv2_img, threshold=127):
            # Convert to grayscale
            grayscale = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)

            # Apply binary threshold
            _, binary = cv2.threshold(grayscale, threshold, 255, cv2.THRESH_BINARY)

            return binary

        # image = np.flip(np.rot90(make_binary(self.paintboard.pixels), k=1), axis=0)
        image = make_binary(self.paintboard.pixels)
        cv2.imwrite('drawing.png', np.flip(np.rot90(make_binary(self.paintboard.pixels), k=1), axis=0))
        return image

    def start_draw_mode(self):
        print("Start draw mode")
        self._draw_mode = True
        self.paintboard.reset()

    def end_draw_mode(self):
        print("End draw mode")
        self._draw_mode = False
        self.paintboard.reset()
