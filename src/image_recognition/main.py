import cv2
from src.image_recognition.to_blackwhite import To_BlackWhite
from src.image_recognition.dimension_getter import Dimension_Getter
from src.image_recognition.ocr import OCR
from src.image_recognition.screenshot import capture_quicktime
from src.image_recognition.cropper import crop, crop_to_focus, extend_image


def save_images(images, main_dir):
    counter = 0
    for img in images:
        cv2.imwrite(main_dir + f'_{counter}.png', img)
        counter += 1


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


def get_two_vector_matrices():
    capture_quicktime('../image_recognition/detection/quicktime_screenshot.png')
    crop('../image_recognition/detection/quicktime_screenshot.png',
         60, 780, 380, 1770,
         '../image_recognition/detection/cropped_image_rows.png')
    crop('../image_recognition/detection/quicktime_screenshot.png',
         385, 460, 1370, 760,
         '../image_recognition/detection/cropped_image_cols.png')
    rows_bw = To_BlackWhite('../image_recognition/detection/cropped_image_rows.png',
                            True,
                            '../image_recognition/detection/cleaned_rows.png').image
    cols_bw = To_BlackWhite('../image_recognition/detection/cropped_image_cols.png',
                            False,
                            '../image_recognition/detection/cleaned_cols.png').image
    crop_to_focus('../image_recognition/detection/cleaned_rows.png',
                  '../image_recognition/detection/focus_cleaned_rows.png')
    crop_to_focus('../image_recognition/detection/cleaned_cols.png',
                  '../image_recognition/detection/focus_cleaned_cols.png')

    rows_dim_getter = Dimension_Getter(rows_bw,
                                       30, 12,
                                       '../image_recognition/detection/focus_cleaned_rows.png',
                                       '../image_recognition/debug/rows.png')
    cols_dim_getter = Dimension_Getter(cols_bw,
                                       30, 10,
                                       '../image_recognition/detection/focus_cleaned_cols.png',
                                       '../image_recognition/debug/cols.png')

    extend_image('../image_recognition/detection/focus_cleaned_rows.png',
                 '../image_recognition/detection/extend_focus_clean_rows.png',
                 top=int(rows_dim_getter.gap_y / 2), bottom=int(rows_dim_getter.gap_y / 2),
                 left=int(rows_dim_getter.gap_x / 2), right=int(rows_dim_getter.gap_x / 2))
    extend_image('../image_recognition/detection/focus_cleaned_cols.png',
                 '../image_recognition/detection/extend_focus_clean_cols.png',
                 top=int(cols_dim_getter.gap_y / 2), bottom=int(cols_dim_getter.gap_y / 2),
                 left=int(cols_dim_getter.gap_x / 2), right=int(cols_dim_getter.gap_x / 2))

    row_img = cv2.imread('../image_recognition/detection/extend_focus_clean_rows.png')
    col_img = cv2.imread('../image_recognition/detection/extend_focus_clean_cols.png')

    rows_ocr = OCR(row_img, rows_dim_getter.dim[0], rows_dim_getter.dim[1], True)
    cols_ocr = OCR(col_img, cols_dim_getter.dim[0], cols_dim_getter.dim[1], False)

    balance_lists(rows_ocr.lists)
    balance_lists(cols_ocr.lists)
    to_int(rows_ocr.lists)
    to_int(cols_ocr.lists)

    return rows_ocr.lists, cols_ocr.lists, rows_dim_getter.dim[0], cols_dim_getter.dim[1]


if __name__ == '__main__':
    capture_quicktime('detection/quicktime_screenshot.png')
    crop('detection/quicktime_screenshot.png',
         60, 780, 380, 1770,
         'detection/cropped_image_rows.png')
    crop('detection/quicktime_screenshot.png',
         385, 460, 1370, 760,
         'detection/cropped_image_cols.png')
    rows_bw = To_BlackWhite('detection/cropped_image_rows.png',
                            True,
                            'detection/cleaned_rows.png').image
    cols_bw = To_BlackWhite('detection/cropped_image_cols.png',
                            False,
                            'detection/cleaned_cols.png').image
    crop_to_focus('detection/cleaned_rows.png', 'detection/focus_cleaned_rows.png')
    crop_to_focus('detection/cleaned_cols.png', 'detection/focus_cleaned_cols.png')

    rows_dim_getter = Dimension_Getter(rows_bw,
                                       30, 12,
                                       'detection/focus_cleaned_rows.png',
                                       'debug/rows.png')
    cols_dim_getter = Dimension_Getter(cols_bw,
                                       30, 10,
                                       'detection/focus_cleaned_cols.png',
                                       'debug/cols.png')

    extend_image('detection/focus_cleaned_rows.png',
                 'detection/extend_focus_clean_rows.png',
                 top=int(rows_dim_getter.gap_y/2), bottom=int(rows_dim_getter.gap_y/2),
                 left=int(rows_dim_getter.gap_x/2), right=int(rows_dim_getter.gap_x/2))
    extend_image('detection/focus_cleaned_cols.png',
                 'detection/extend_focus_clean_cols.png',
                 top=int(cols_dim_getter.gap_y/2), bottom=int(cols_dim_getter.gap_y/2),
                 left=int(cols_dim_getter.gap_x/2), right=int(cols_dim_getter.gap_x/2))

    row_img = cv2.imread('detection/extend_focus_clean_rows.png')
    col_img = cv2.imread('detection/extend_focus_clean_cols.png')

    rows_ocr = OCR(row_img, rows_dim_getter.dim[0], rows_dim_getter.dim[1], True)
    cols_ocr = OCR(col_img, cols_dim_getter.dim[0], cols_dim_getter.dim[1], False)

    # save_images(rows_ocr.section, 'debug/rows_divide/out')
    # save_images(cols_ocr.section, 'debug/cols_divide/out')
