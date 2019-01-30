import os
import sys


def get_app_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(__file__)


def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    See https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
