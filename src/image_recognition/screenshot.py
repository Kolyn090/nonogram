import platform
import cv2
if platform.system() == "Darwin":
    import mss
    import Quartz
import numpy as np


class Screenshot:
    def __init__(self, window_name: str):
        def get_window_bounds(window_name):
            """Find the QuickTime Player window's bounds."""
            options = Quartz.kCGWindowListOptionOnScreenOnly
            window_list = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)

            for window in window_list:
                # Match the application name (case-insensitive)
                if window_name.lower() in window.get('kCGWindowOwnerName', '').lower():
                    print(f"Found window: {window['kCGWindowOwnerName']}")
                    bounds = window['kCGWindowBounds']
                    return bounds  # {'X': ..., 'Y': ..., 'Width': ..., 'Height': ...}

            raise Exception(f"Window '{window_name}' not found.")

        def capture(window_name):
            """Capture the screenshot of QuickTime Player."""
            try:
                bounds = get_window_bounds(window_name)
                with mss.mss() as sct:
                    monitor = {
                        "top": bounds['Y'],
                        "left": bounds['X'],
                        "width": bounds['Width'],
                        "height": bounds['Height'],
                    }
                    screenshot = sct.grab(monitor)
                    # Convert the screenshot to PNG bytes
                    png_bytes = mss.tools.to_png(screenshot.rgb, screenshot.size)

                    # Decode the PNG bytes to a NumPy array (OpenCV image)
                    png_array = np.frombuffer(png_bytes, dtype=np.uint8)
                    image_bgr = cv2.imdecode(png_array, cv2.IMREAD_COLOR)

                    return image_bgr
            except Exception as e:
                print(f"Error: {e}")

        self.image = capture(window_name)


if __name__ == '__main__':
    screenshot = Screenshot("QuickTime Player")
    cv2.imwrite('test/screenshot/quicktime.png', screenshot.image)
