from PIL import Image
import cv2
import numpy as np


def crop(image_path, left, upper, right, lower, write_path):
    # Open the image
    image = Image.open(image_path)

    # Define the cropping area (left, upper, right, lower)
    crop_area = (left, upper, right, lower)  # Example coordinates

    # Crop the image
    cropped_image = image.crop(crop_area)

    # Show the cropped image (optional)
    # cropped_image.show()

    # Save the cropped image
    cropped_image.save(write_path)


def crop_to_focus(image_path, write_path, min_black_blob_size=100):
    """
    Crops as much white space as possible from an image with black and white pixels,
    ignoring small black blobs (noise) below a specified size.

    :param image_path: Path to the input image.
    :param write_path: Path to save the cropped image.
    :param min_black_blob_size: Minimum area of black blobs to keep.
    """
    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print(f"Error: Unable to load image from {image_path}.")
        return

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

    # Save the cropped image
    cv2.imwrite(write_path, cropped_image)
    # print(f"Cropped image saved at {output_path}.")


def extend_image(image_path, output_path, top=0, bottom=0, left=0, right=0, color=(255, 255, 255)):
    """
    Extends the image size by adding padding along the x and y axes, filling the new space with white or any other color.

    :param image_path: Path to the input image.
    :param output_path: Path to save the extended image.
    :param top: Number of pixels to add to the top.
    :param bottom: Number of pixels to add to the bottom.
    :param left: Number of pixels to add to the left.
    :param right: Number of pixels to add to the right.
    :param color: Padding color, default is white (255, 255, 255) for RGB.
    """
    # Load the image
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Unable to load image from {image_path}.")
        return
    # Use copyMakeBorder to extend the image
    extended_image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

    # Save the extended image
    cv2.imwrite(output_path, extended_image)
    # print(f"Extended image saved at {output_path}.")
    return extended_image
