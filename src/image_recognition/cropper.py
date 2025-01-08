import cv2
import numpy as np
from src.image_recognition.binarizer import convert_to_grayscale


class Cropper:
    @staticmethod
    def crop(image, bbox):
        left = bbox[0]
        top = bbox[1]
        right = bbox[2]
        bottom = bbox[3]
        return image[top:bottom, left:right]

    @staticmethod
    def trim(image, min_black_blob_size=100):
        """
        Crops as much white space as possible from an image with black and white pixels,
        ignoring small black blobs (noise) below a specified size.

        @:param image: The input image.
        @:param min_black_blob_size: Minimum area of black blobs to keep.

        @:return Cropped cv2 image
        """
        image = convert_to_grayscale(image)

        # Ensure the image contains only black (0) and white (255) pixels
        _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

        # Invert the binary image so black becomes white (foreground) and white becomes black
        inverted = cv2.bitwise_not(binary)

        # Find contours in the inverted image
        contours, _ = cv2.findContours(inverted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter out small black blobs (noise)
        valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) >= min_black_blob_size]

        if not valid_contours:
            print("No valid black regions found.")
            return

        # Compute the bounding box that encloses all valid black blobs
        x_min, y_min = np.inf, np.inf
        x_max, y_max = -np.inf, -np.inf

        for cnt in valid_contours:
            x, y, w, h = cv2.boundingRect(cnt)
            x_min = min(x_min, x)
            y_min = min(y_min, y)
            x_max = max(x_max, x + w)
            y_max = max(y_max, y + h)

        # Crop the image to the bounding box
        cropped_image = image[int(y_min):int(y_max), int(x_min):int(x_max)]

        return cropped_image

    @staticmethod
    def extend_image(image, top=0, bottom=0, left=0, right=0, padding_color=(255, 255, 255)):
        """
        Extends the image size by adding padding along the x and y axes, filling the new space with white or any other color.

        :param image: The input image.
        :param top: Number of pixels to add to the top.
        :param bottom: Number of pixels to add to the bottom.
        :param left: Number of pixels to add to the left.
        :param right: Number of pixels to add to the right.
        :param padding_color: Padding color, default is white (255, 255, 255) for RGB.
        """

        return cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=padding_color)
