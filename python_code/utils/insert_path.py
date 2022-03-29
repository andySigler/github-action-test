import os
import sys


def insert_path(file, relative_path):
    file_dir = os.path.dirname(os.path.abspath(file))
    path_to_insert = os.path.join(file_dir, relative_path)
    sys.path.insert(0, path_to_insert)
