import argparse

import git
from PyInstaller.__main__ import run as build_exe


if __name__ == '__main__':
    '''
    FILE_NAME="$1"
    SCRIPT_DIR="$THIS_DIR/python_test/tests/$FILE_NAME"

    # TODO: generate temporary .version file containing git hash

    SCRIPT_PATH="$SCRIPT_DIR/__main__.py"
    VERSION_FILE_NAME="$SCRIPT_DIR/.version"

    # TODO: append .version to the executable's file name

    BUILD_PATH="$THIS_DIR/build"
    OUTPUT_PATH="$BUILD_PATH/$FILE_NAME"

    # erase previous build folder
    rm -rf "$BUILD_PATH" || true
    # build
    pyinstaller "$SCRIPT_PATH" --clean --onefile --name "$OUTPUT_PATH" --distpath "$THIS_DIR" -y --add-data "$VERSION_FILE_NAME:."
    '''
    parser = argparse.ArgumentParser("Script Build")
    parser.add_argument(
        "-n",
        "--name",
        help="Script name",
        default="",
        type=str,
    )
    parser.add_argument(
        "-o",
        "--out-dir",
        help="Path to output directory",
        default="./build",
        type=str,
    )
    # parser.add_argument('-r', '--release', action='store_true')
    args = parser.parse_args()
    # TODO: find test based on --name (might be multiple)
    # TODO: read .version, and check if we are a release
    # TODO: generate temporary .version file (using git-hash)
    # TODO: build PyInstaller executable
