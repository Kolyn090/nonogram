import cv2
from to_blackwhite import To_BlackWhite
from dimension_getter import Dimension_Getter
from ocr import OCR
from screenshot import capture_quicktime
from croper import crop


def save_images(images, main_dir):
    counter = 0
    for img in images:
        cv2.imwrite(main_dir + f'_{counter}.png', img)
        counter += 1


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
    rows_dim_getter = Dimension_Getter(rows_bw,
                                       0,2,
                                       'detection/cleaned_rows.png',
                                       'debug/rows.png')
    cols_dim_getter = Dimension_Getter(cols_bw,
                                       30,5,
                                       'detection/cleaned_cols.png',
                                       'debug/cols.png')
    rows_ocr = OCR(rows_bw, rows_dim_getter.dim[0], True)
    cols_ocr = OCR(cols_bw, cols_dim_getter.dim[1], False)

    save_images(rows_ocr.section, 'debug/rows_divide/out')
    save_images(cols_ocr.section, 'debug/cols_divide/out')
