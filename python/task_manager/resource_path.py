import os
import sys


def resource_path(relative_path):
    # function for image paths pyinstaller related
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(r"img\\.")

    return os.path.join(base_path, relative_path)