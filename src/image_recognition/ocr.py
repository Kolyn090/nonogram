from pytesseract import pytesseract
import cv2


class OCR:
    def __init__(self, bw_img, width, height, is_divided_horizontally=True):
        def divide_image_vertically(image, factor=2):
            """
            Divides an image vertically by a given factor and saves the sections.
            Args:
                image: The image.
                factor: The number of vertical splits to make.
            """
            # Get the height and width of the image
            height, width = image.shape[:2]

            # Calculate the width of each section
            section_width = width // factor

            result = []

            # Loop to split and save each section
            for i in range(factor):
                # Calculate the x-coordinates for the section
                x_start = i * section_width
                x_end = (i + 1) * section_width if i < factor - 1 else width

                # Slice the image horizontally
                section = image[:, x_start:x_end]

                # Generate a filename for the section
                # section_filename = os.path.join(output_folder, f"section_{i + 1}.png")

                result.append(section)

            return result

        def divide_image_horizontally(image, factor=2):
            """
            Divides an image vertically by a given factor and saves the sections.
            Args:
                image: The image.
                factor: The number of vertical splits to make.
            """
            # Get the height and width of the image
            height, width = image.shape[:2]

            # Calculate the width of each section
            section_height = height // factor

            result = []

            # Loop to split and save each section
            for i in range(factor):
                # Calculate the y-coordinates for the section
                y_start = i * section_height
                y_end = (i + 1) * section_height if i < factor - 1 else height

                # Slice the image horizontally (by rows)
                section = image[y_start:y_end, :]

                # Add the section to the result list
                result.append(section)

            return result

        if is_divided_horizontally:
            self.section = divide_image_horizontally(bw_img, height)
            self.image_grid = []

            # count = 0
            for img in self.section:
                num_row = divide_image_vertically(img, width)
                # for piece in num_row:
                #     cv2.imwrite(f'debug/grid/out_{count}.png', piece)
                #     count += 1
                self.image_grid.append(num_row)
        else:
            self.section = divide_image_vertically(bw_img, width)
            self.image_grid = []

            # count = 0
            for img in self.section:
                num_row = divide_image_horizontally(img, height)
                # for piece in num_row:
                #     cv2.imwrite(f'debug/grid/out_{count}.png', piece)
                #     count += 1
                self.image_grid.append(num_row)

        custom_config = r'--oem 3 --psm 6 outputbase digits'

        self.lists = []
        for image_list in self.image_grid:
            row = []
            for image in image_list:
                digits = pytesseract.image_to_string(image, config=custom_config)
                str_num = ''.join([str(digit) for digit in digits if digit in '0123456789'])
                if str_num:
                    num = int(str_num)
                    row.append(num)
            self.lists.append(row)
        print(self.lists)
