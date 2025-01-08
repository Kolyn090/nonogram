import cv2
import numpy
import numpy as np


def convert_to_grayscale(image):
    """
    Converts any OpenCV image (color, alpha, etc.) to grayscale.

    Args:
        image: The OpenCV image (numpy array).

    Returns:
        Grayscale image (numpy array).
    """
    # If the image has 3 channels (e.g., BGR), convert to grayscale
    if len(image.shape) == 3 and image.shape[2] == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # If the image has 4 channels (e.g., BGRA), convert to grayscale
    elif len(image.shape) == 3 and image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    # If already grayscale, return as-is
    elif len(image.shape) == 2:
        return image
    else:
        raise ValueError("Unsupported image format for grayscale conversion.")


class Binarizer:
    """
    Takes a screenshot of digit matrix and extract the digits with binarization.

    @:param image: The screenshot
    @:param is_rows: Treat the matrix as Nonogram rows
    """
    def __init__(self, image: numpy.ndarray, is_rows: bool):
        def binary_preprocess(image):
            """Detects black edges and filters small contours to only detect valid rows."""
            # Apply the extreme contrast adjustment
            adjusted = cv2.convertScaleAbs(image, alpha=3, beta=-90)

            adjusted = cv2.convertScaleAbs(adjusted, alpha=2, beta=-90)

            # Normalize pixel values to range [0, 1]
            normalized = adjusted / 255.0

            # Apply gamma correction (values below 1 are darkened more)
            gamma_corrected = np.power(normalized, 10)

            # Rescale back to [0, 255] and convert to uint8
            result = np.uint8(gamma_corrected * 255)

            return result

        def remove_residual_lines(image, is_rows):
            """Removes residual lines using morphological operations."""
            # Step 1: Apply binary thresholding to separate text and lines
            _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

            # Step 2: Detect vertical lines using a larger vertical kernel
            vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 21))  # Kernel for line detection
            detected_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

            # Step 3: Dilate the detected lines to ensure full line coverage
            dilated_lines = cv2.dilate(detected_lines, vertical_kernel, iterations=16)

            # Step 4: Subtract the detected lines from the original binary image
            lines_removed = cv2.subtract(binary, dilated_lines)

            # Step 5: Perform a final cleanup using closing to smooth any artifacts
            horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,
                                                          (5, 1))  # Horizontal kernel to preserve text structure
            cleaned_image = cv2.morphologyEx(lines_removed, cv2.MORPH_CLOSE, horizontal_kernel, iterations=1)

            if is_rows:
                """Perform an extra check to remove stubborn horizontal lines"""
                # Step 1: Detect horizontal lines using a horizontal kernel
                horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))  # Kernel for horizontal lines
                detected_lines = cv2.morphologyEx(lines_removed, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

                # Step 2: Dilate the detected lines to ensure full coverage
                dilated_lines = cv2.dilate(detected_lines, horizontal_kernel, iterations=16)

                # Step 3: Subtract the detected lines from the original binary mask
                lines_removed = cv2.subtract(binary, dilated_lines)

                # Step 4: Invert the result to restore the original text on white background
                cleaned_image = lines_removed

            # Invert the result to get the final cleaned image
            final_result = cv2.bitwise_not(cleaned_image)

            return final_result

        self.image = binary_preprocess(convert_to_grayscale(image))
        self.image = remove_residual_lines(self.image, is_rows)


if __name__ == '__main__':
    rows_binary = Binarizer(cv2.imread('test/binarizer/cropped_image_rows.png'), True).image
    cv2.imwrite('test/binarizer/rows_binary.png', rows_binary)
    cols_binary = Binarizer(cv2.imread('test/binarizer/cropped_image_cols.png'), False).image
    cv2.imwrite('test/binarizer/cols_binary.png', cols_binary)
