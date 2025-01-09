import cv2
from src.solve.solution import EMPTY_MARKER, FILL_MARKER


class Binary_To_Ascii_Art:
    def __init__(self, binary_image):
        self.EMPTY_MARKER = EMPTY_MARKER
        self.FILL_MARKER = FILL_MARKER
        height, width = binary_image.shape

        self.ascii = []
        self.pixels = []
        # Iterate through each pixel
        for y in range(height):  # Rows
            row = []
            pixel_row = []
            for x in range(width):  # Columns
                pixel_value = binary_image[y, x]
                # Check if the pixel is black or white
                if pixel_value == 255:
                    row.append(EMPTY_MARKER)
                    pixel_row.append(False)
                elif pixel_value == 0:
                    row.append(FILL_MARKER)
                    pixel_row.append(True)
            self.ascii.append(row)
            self.pixels.append(pixel_row)


if __name__ == '__main__':
    binary_image = cv2.imread('binary.png', cv2.THRESH_BINARY)
    btaa = Binary_To_Ascii_Art(binary_image)
    # for lst in btaa.ascii:
    #     print(''.join(lst))
    for lst in btaa.pixels:
        print(''.join(str(lst)))
