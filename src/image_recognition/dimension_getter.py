import cv2
from src.image_recognition.binarizer import Binarizer


class Dimension_Getter:
    def __init__(self, image, vib_x, vib_y, image_name=None, write_path='debug/img.png'):
        # The gap distances between each number
        self.gap_x = 0
        self.gap_y = 0

        def get_snap_positions(pos_lst, vib_x, vib_y):
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

            def snap_positions():
                pos_lst_sortx = sorted(pos_lst)

                curr_x = pos_lst_sortx[0][0]
                for i in range(len(pos_lst_sortx)):
                    pos = pos_lst_sortx[i]
                    pos_x = pos[0]
                    if abs(curr_x - pos_x) < vib_x:
                        pos_lst_sortx[i] = (curr_x, pos[1])
                    else:
                        curr_x = pos_x
                pos_lstx_sorty = sorted(pos_lst_sortx)
                curr_y = pos_lstx_sorty[0][1]
                for i in range(len(pos_lstx_sorty)):
                    pos = pos_lstx_sorty[i]
                    pos_y = pos[1]
                    if abs(curr_y - pos_y) < vib_y:
                        pos_lstx_sorty[i] = (pos[0], curr_y)
                    else:
                        curr_y = pos_y
                return pos_lstx_sorty

            snapped_pos_lst = snap_positions()

            if image_name is not None:
                # debug mode
                img = cv2.imread(image_name)
                for pos in snapped_pos_lst:
                    cv2.circle(img, pos, 2, (0, 0, 255), 2)
                cv2.imwrite(write_path, img)

            return snapped_pos_lst

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
            total_w = 0
            total_h = 0
            for c in row_contours:
                x, y, w, h = cv2.boundingRect(c)
                pos_lst.append((x, y))
                total_w += w
                total_h += h
                cv2.rectangle(debug_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imwrite(write_path.replace('.png', '_debug.png'), debug_image)

            snapped_pos_lst = get_snap_positions(pos_lst, vib_x, vib_y)
            all_x = set([pos[0] for pos in snapped_pos_lst])
            all_y = set([pos[1] for pos in snapped_pos_lst])
            lst_x = list(all_x)
            lst_y = list(all_y)

            def calculate_gap_average(lst):
                total = 0
                sorted_lst = sorted(lst, reverse=True)
                for i in range(1, len(sorted_lst)):
                    total += sorted_lst[i] - sorted_lst[i-1]
                return abs(total // max(len(sorted_lst)-1, 1))

            self.gap_x = abs(calculate_gap_average(lst_x) - total_w//(len(row_contours)-1))
            self.gap_y = abs(calculate_gap_average(lst_y) - total_h//(len(row_contours)-1))
            return len(all_x), len(all_y)

        self.dim = get_dimension(image, vib_x, vib_y)


if __name__ == '__main__':
    rows_bw = Binarizer('detection/cropped_image_rows.png', True, 'detection/cleaned_rows.png').image
    rows_dim_getter = Dimension_Getter(rows_bw, 0, 2, 'detection/cleaned_rows.png', 'debug/rows.png')

    cols_bw = Binarizer('detection/cropped_image_cols.png', False, 'detection/cleaned_cols.png').image
    cols_dim_getter = Dimension_Getter(cols_bw, 30, 5, 'detection/cleaned_cols.png', 'debug/cols.png')

    print(rows_dim_getter.dim)
    print(cols_dim_getter.dim)
