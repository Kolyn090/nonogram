import cv2
import numpy as np


class To_BlackWhite:
    def __init__(self, image_path, is_focusing_rows, write_path):
        def convert_to_black_white(image_path):
            """Detects black edges and filters small contours to only detect valid rows."""
            # Load the image in grayscale
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

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

        def remove_residual_lines(image, is_focusing_rows):
            """Removes residual lines using morphological operations."""
            # Step 1: Apply binary thresholding to separate text and lines
            _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

            # Step 2: Detect vertical lines using a larger vertical kernel
            vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))  # Kernel for line detection
            detected_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

            # Step 3: Dilate the detected lines to ensure full line coverage
            dilated_lines = cv2.dilate(detected_lines, vertical_kernel, iterations=2)

            # Step 4: Subtract the detected lines from the original binary image
            lines_removed = cv2.subtract(binary, dilated_lines)

            # Step 5: Perform a final cleanup using closing to smooth any artifacts
            horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,
                                                          (5, 1))  # Horizontal kernel to preserve text structure
            cleaned_image = cv2.morphologyEx(lines_removed, cv2.MORPH_CLOSE, horizontal_kernel, iterations=1)

            if is_focusing_rows:
                """Perform an extra check to remove stubborn horizontal lines"""
                # Step 1: Detect horizontal lines using a horizontal kernel
                horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))  # Kernel for horizontal lines
                detected_lines = cv2.morphologyEx(lines_removed, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

                # Step 2: Dilate the detected lines to ensure full coverage
                dilated_lines = cv2.dilate(detected_lines, horizontal_kernel, iterations=2)

                # Step 3: Subtract the detected lines from the original binary mask
                lines_removed = cv2.subtract(binary, dilated_lines)

                # Step 4: Invert the result to restore the original text on white background
                cleaned_image = lines_removed

            # Invert the result to get the final cleaned image
            final_result = cv2.bitwise_not(cleaned_image)
            cv2.imwrite(write_path, final_result)

            return final_result

        black_white_image = convert_to_black_white(image_path)
        self.image = remove_residual_lines(black_white_image, is_focusing_rows)
