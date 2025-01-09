import cv2
from src.solve.description import Description
from src.draw.binary_to_ascii_art import Binary_To_Ascii_Art


class Pixels_To_Description:
    def __init__(self, pixels):
        self.description = Description()
        self.description.width = len(pixels)
        self.description.height = len(pixels[0])
        self.pixels = pixels
        self.description.row_descriptions = [self.get_row_description(y) for y in range(self.description.height)]
        self.description.column_descriptions = [self.get_col_description(x) for x in range(self.description.width)]

    def get_row_description(self, y):
        result = []
        cum = 0
        for x in range(self.description.width):
            if self.pixels[x][y]:
                cum += 1
            elif cum > 0:
                result.append(cum)
                cum = 0
        if cum > 0:
            result.append(cum)
        return result

    def get_col_description(self, x):
        result = []
        cum = 0
        for y in range(self.description.height):
            if self.pixels[x][y]:
                cum += 1
            elif cum > 0:
                result.append(cum)
                cum = 0
        if cum > 0:
            result.append(cum)
        return result


if __name__ == '__main__':
    binary_image = cv2.imread('binary.png', cv2.THRESH_BINARY)
    btaa = Binary_To_Ascii_Art(binary_image)
    ptd = Pixels_To_Description(btaa.pixels)
    description = ptd.description
    print(description.row_descriptions)
    print(description.column_descriptions)
