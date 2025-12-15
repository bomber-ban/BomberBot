# /home/xty/Documents/Projects/PetProject/BomberBot_GUI/BomberBot_GUI/gui/utils.py
import sys
import os


def resource_path(relative_path: str) -> str:
    if getattr(sys, 'frozen', False):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.dirname(current_dir)

    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if relative_path.startswith(os.path.sep) or relative_path.startswith('/'):
        return relative_path

    return os.path.join(base_path, relative_path)
