import cv2


def draw_custom_grid(image_path, output_path, rows, cols, line_color=(0, 255, 0), thickness=1):
    """
    Draws a grid with a specified number of rows and columns on the given image.

    :param image_path: Path to the input image.
    :param output_path: Path to save the image with grid lines.
    :param rows: Number of horizontal divisions (grid rows).
    :param cols: Number of vertical divisions (grid columns).
    :param line_color: Color of the grid lines in BGR (default: green).
    :param thickness: Thickness of the grid lines.
    """
    # Load the image
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Unable to load image from {image_path}.")
        return

    # Get the dimensions of the image
    height, width, _ = image.shape

    # Calculate the size of each cell
    row_height = height // rows
    col_width = width // cols

    # Draw vertical grid lines
    for col in range(1, cols):
        x = col * col_width
        cv2.line(image, (x, 0), (x, height), line_color, thickness)

    # Draw horizontal grid lines
    for row in range(1, rows):
        y = row * row_height
        cv2.line(image, (0, y), (width, y), line_color, thickness)

    # Save the image with grid lines
    cv2.imwrite(output_path, image)
    print(f"Grid image saved at {output_path}.")


if __name__ == '__main__':
    draw_custom_grid('detection/extend_focus_clean_rows.png', 'debug/rows_grid.png', 8, 2)
    draw_custom_grid('detection/extend_focus_clean_cols.png', 'debug/cols_grid.png', 2, 8)
