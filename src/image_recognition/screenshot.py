import Quartz
import mss


def get_window_bounds(window_name="QuickTime Player"):
    """Find the QuickTime Player window's bounds."""
    options = Quartz.kCGWindowListOptionOnScreenOnly
    window_list = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)

    for window in window_list:
        # Match the application name (case insensitive)
        if window_name.lower() in window.get('kCGWindowOwnerName', '').lower():
            print(f"Found window: {window['kCGWindowOwnerName']}")
            bounds = window['kCGWindowBounds']
            return bounds  # {'X': ..., 'Y': ..., 'Width': ..., 'Height': ...}

    raise Exception(f"Window '{window_name}' not found.")


def capture_quicktime(output_file="quicktime_screenshot.png"):
    """Capture the screenshot of QuickTime Player."""
    try:
        bounds = get_window_bounds()
        with mss.mss() as sct:
            monitor = {
                "top": bounds['Y'],
                "left": bounds['X'],
                "width": bounds['Width'],
                "height": bounds['Height'],
            }
            screenshot = sct.grab(monitor)
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=output_file)
            print(f"Screenshot saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")


# Example usage:
# capture_quicktime()

# options = Quartz.kCGWindowListOptionOnScreenOnly
# window_list = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)
# for window in window_list:
#     print(window)
