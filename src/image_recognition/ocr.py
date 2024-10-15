import cv2
from pytesseract import pytesseract
from image_recognition.dimension_getter import Dimension_Getter
from to_blackwhite import To_BlackWhite


class OCR:
    def __init__(self, bw_img, factor, is_divided_horizontally=True):
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
            self.section = divide_image_horizontally(bw_img, factor)
        else:
            self.section = divide_image_vertically(bw_img, factor)

        custom_config = r'--oem 3 --psm 6 outputbase digits'

        self.lists = []
        for img in self.section:
            digits = pytesseract.image_to_string(img, config=custom_config)
            self.lists.append([digit for digit in digits if digit in '0123456789'])
