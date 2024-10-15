from PIL import Image


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


# crop(60, 780, 380, 1770, 'cropped_image_rows.png')
# crop(385, 460, 1370, 760, 'cropped_image_cols.png')
