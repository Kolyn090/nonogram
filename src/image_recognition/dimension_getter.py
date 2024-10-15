import cv2
from src.image_recognition.to_blackwhite import To_BlackWhite


class Dimension_Getter:
    def __init__(self, image, vib_x, vib_y, image_name=None, write_path='debug/img.png'):
        def get_matrix_len(pos_lst, vib_x, vib_y):
            """

            :param pos_lst: a list of tuples of (x, y) position
            :param vib_x: vibration for x (assimilate if within range)
            :param vib_y: vibration for y (assimilate if within range)
            :return: total number of rows and total number of columns
            """

            curr_y = pos_lst[0][1]
            for i in range(len(pos_lst)):
                pos = pos_lst[i]
                pos_y = pos[1]
                if abs(curr_y - pos_y) < vib_y:
                    pos_lst[i] = (pos[0], curr_y)
                else:
                    curr_y = pos_y

            curr_x = pos_lst[0][0]
            for i in range(len(pos_lst)):
                pos = pos_lst[i]
                pos_x = pos[0]
                if abs(curr_x - pos_x) < vib_x:
                    pos_lst[i] = (curr_x, pos[1])
                else:
                    curr_x = pos_x

            if image_name is not None:
                # debug mode
                img = cv2.imread(image_name)
                for pos in pos_lst:
                    cv2.circle(img, pos, 2, (0, 0, 255), 2)
                cv2.imwrite(write_path, img)

            row_ys = set()
            for pos in pos_lst:
                row_ys.add(pos[1])
            total_rows = len(row_ys)

            total_cols = 0
            for row_y in row_ys:
                level = [pos for pos in pos_lst if pos[1] == row_y]
                cols = 1
                curr_x = level[0][0]
                for i in range(len(level)):
                    pos = level[i]
                    pos_x = pos[0]
                    if pos_x != curr_x:
                        curr_x = pos_x
                        cols += 1
                if cols > total_cols:
                    total_cols = cols

            return total_rows, total_cols

        def get_dimension(image, vib_x, vib_y):
            """Detects the number of rows more accurately by using contours and filtering."""
            # Apply Gaussian blur to smooth out noise and small gaps
            blurred = cv2.GaussianBlur(image, (5, 5), 0)

            # Apply binary inverse thresholding
            _, thresh = cv2.threshold(blurred, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

            # Find contours from the thresholded image
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Filter out small contours (noise)
            # Height > 10 pixels & Width > 10 pixels
            row_contours = [c for c in contours if cv2.boundingRect(c)[3] > 10 and cv2.boundingRect(c)[2] > 10]

            # Sort the contours by their y-coordinate (top to bottom)
            row_contours = sorted(row_contours, key=lambda c: cv2.boundingRect(c)[1])

            # Optional: Draw bounding boxes around detected rows for debugging
            debug_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            pos_lst = []
            for c in row_contours:
                x, y, w, h = cv2.boundingRect(c)
                pos_lst.append((x, y))
                cv2.rectangle(debug_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imwrite(write_path.replace('.png', '_debug.png'), debug_image)

            return get_matrix_len(pos_lst, vib_x, vib_y)

        self.dim = get_dimension(image, vib_x, vib_y)


if __name__ == '__main__':
    rows_bw = To_BlackWhite('detection/cropped_image_rows.png', True, 'detection/cleaned_rows.png').image
    rows_dim_getter = Dimension_Getter(rows_bw, 0, 2, 'detection/cleaned_rows.png', 'debug/rows.png')

    cols_bw = To_BlackWhite('detection/cropped_image_cols.png', False, 'detection/cleaned_cols.png').image
    cols_dim_getter = Dimension_Getter(cols_bw, 30, 5, 'detection/cleaned_cols.png', 'debug/cols.png')

    print(rows_dim_getter.dim)
    print(cols_dim_getter.dim)
