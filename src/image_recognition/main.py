import cv2
from src.image_recognition.ocr import OCR
from src.image_recognition.cropper import Cropper
from src.image_recognition.binarizer import Binarizer
from src.image_recognition.screenshot import Screenshot
from src.image_recognition.dimension_getter import Dimension_Getter
from src.image_recognition.ui_position import top_matrix_region, bottom_matrix_region


def get_two_vector_matrices():
    def balance_lists(lists):
        # fill with 0 if a list is short
        max_len = 0
        for lst in lists:
            if len(lst) > max_len:
                max_len = len(lst)
        for lst in lists:
            while len(lst) < max_len:
                lst.insert(0, 0)

    def to_int(lists):
        for i in range(len(lists)):
            lists[i] = [int(s) for s in lists[i]]

    screenshot = Screenshot("QuickTime Player").image
    # screenshot = cv2.imread('test/screenshot/quicktime_screenshot.png')

    cropper = Cropper()
    matrix_region1 = cropper.crop(screenshot, top_matrix_region)
    matrix_region2 = cropper.crop(screenshot, bottom_matrix_region)

    rows_binary = Binarizer(matrix_region1, True).image
    cols_binary = Binarizer(matrix_region2, False).image

    rows_binary_trimmed = cropper.trim(rows_binary)
    cols_binary_trimmed = cropper.trim(cols_binary)

    rows_dim_getter = Dimension_Getter(rows_binary_trimmed, 30, 12)
    cols_dim_getter = Dimension_Getter(cols_binary_trimmed, 30, 10)

    rows_img = cropper.extend_image(rows_binary_trimmed,
                                    top=int(rows_dim_getter.gap_y / 2), bottom=int(rows_dim_getter.gap_y / 2),
                                    left=int(rows_dim_getter.gap_x / 2), right=int(rows_dim_getter.gap_x / 2))

    cols_img = cropper.extend_image(cols_binary_trimmed,
                                    top=int(cols_dim_getter.gap_y / 2), bottom=int(cols_dim_getter.gap_y / 2),
                                    left=int(cols_dim_getter.gap_x / 2), right=int(cols_dim_getter.gap_x / 2))

    rows_ocr = OCR(rows_img, rows_dim_getter.dim[0], rows_dim_getter.dim[1], True)
    cols_ocr = OCR(cols_img, cols_dim_getter.dim[0], cols_dim_getter.dim[1], False)

    balance_lists(rows_ocr.lists)
    balance_lists(cols_ocr.lists)
    to_int(rows_ocr.lists)
    to_int(cols_ocr.lists)

    return rows_ocr.lists, cols_ocr.lists, rows_dim_getter.dim[0], cols_dim_getter.dim[1]


if __name__ == '__main__':
    result = get_two_vector_matrices()
    print(result[0])
    print(result[1])
    print(result[2])
    print(result[3])
