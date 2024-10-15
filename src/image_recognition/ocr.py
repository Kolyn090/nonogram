import pytesseract
import cv2
from detection.dimension_getter import Dimension_Getter
from to_blackwhite import To_BlackWhite


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


def save_images(images, main_dir):
    counter = 0
    for img in images:
        cv2.imwrite(main_dir + f'_{counter}.png', img)
        counter += 1


rows_bw = To_BlackWhite('cropped_image_rows.png', True, 'detection/cleaned_rows.png').image
cols_bw = To_BlackWhite('cropped_image_cols.png', False, 'detection/cleaned_cols.png').image
rows_dim = Dimension_Getter(rows_bw, 0, 2, 'detection/cleaned_rows.png', 'debug/rows.png').dim
cols_dim = Dimension_Getter(cols_bw, 30, 5, 'detection/cleaned_cols.png', 'debug/cols.png').dim
rows_section = divide_image_horizontally(rows_bw, rows_dim[0])
cols_section = divide_image_vertically(cols_bw, cols_dim[1])

# print(rows_dim)
print(cols_dim)

# custom_config = r'--oem 3 --psm 6 outputbase digits'
# for img in cols_section:
#     digits = pytesseract.image_to_string(img, config=custom_config)
#     print("Extracted Digits:", [digit for digit in digits if digit != '\n'])
#
# save_images(rows_section, 'rows_divide/out')
# save_images(cols_section, 'cols_divide/out')
