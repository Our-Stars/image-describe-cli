"""Screenshot module. Cross-platform full-screen capture (mss) and macOS window capture (screencapture)."""
import os
import sys
import subprocess
import tempfile
from datetime import datetime


def _capture_dir():
    path = os.path.expanduser("~/.config/image-describe/captures")
    os.makedirs(path, exist_ok=True)
    return path


def _generate_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(_capture_dir(), f"screenshot_{timestamp}.png")


def _capture_full_screen_bytes():
    from mss import mss
    from mss.tools import to_png

    with mss() as sct:
        sct_img = sct.grab(sct.monitors[0])
        return to_png(sct_img.rgb, sct_img.size)


def _capture_window_macos_bytes(window_id):
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    tmp_path = tmp.name
    tmp.close()
    try:
        subprocess.run(
            ["screencapture", "-l", str(window_id), "-x", tmp_path],
            check=True,
            capture_output=True,
        )
        with open(tmp_path, "rb") as f:
            return f.read()
    finally:
        os.unlink(tmp_path)


def capture_bytes(window_id=None):
    """Capture as PNG bytes, entirely in memory (no disk writes).

    On macOS with window_id, uses screencapture to a temp file that is
    immediately deleted after reading.
    """
    if window_id is not None and sys.platform == "darwin":
        return _capture_window_macos_bytes(window_id)
    else:
        return _capture_full_screen_bytes()


def capture(output_path=None, window_id=None):
    """Capture screenshot and save to file. Returns absolute path."""
    if output_path is None:
        output_path = _generate_filename()

    png_bytes = capture_bytes(window_id)
    with open(output_path, "wb") as f:
        f.write(png_bytes)

    return os.path.abspath(output_path)
