import argparse
import os

import git
from PyInstaller.__main__ import run as build_exe

from .script_version import VERSION_FILE_NAME, read_version_file, get_git_commit_hash, DEFAULT_HASH_LENGTH


SCRIPT_FILE_NAME = '__main__.py'  # all test scripts are named __main__.py


def generate_version_tag(name, version):
    return name + '_' + version


def add_commit_to_version_name(name, hash):
    return name + hash[:DEFAULT_HASH_LENGTH]


def search_for_subfolder_by_name(parent_dir, subfolder_name):
    matching_dirs = []
    for d in os.listdir(parent_dir):
        abs_path = os.path.abspath(os.path.join(parent_dir, d))
        if os.path.isdir(abs_path):
            if d == subfolder_name:
                matching_dirs.append(abs_path)
            matching_dirs += search_for_subfolder_by_name(abs_path, subfolder_name)
    return matching_dirs


def is_commit_a_release(repo, expected_tag_name, commit_hash):
    for tag in repo.tags:
        same_hash = (str(tag.commit) == commit_hash)
        same_version = (expected_tag_name == str(tag))
        if same_hash and same_version:
            return True
        elif same_hash:
            raise ValueError(
                f'Expected tag name ({expected_tag_name}) does not match tag at this commit: {str(tag)}')
        elif same_version:
            # NOTE: this is expected during development, because version numbers only change with new releases
            continue
    return False


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
    scripts_dir = os.path.join(os.path.dirname(__file__), '../scripts')
    matching_dirs = search_for_subfolder_by_name(scripts_dir, args.name)
    if not len(matching_dirs):
        raise ValueError(f'No script subfolders found named \"{args.name}\"')
    if len(matching_dirs) > 1:
        # TODO: maybe make a list to pick which one to build?
        raise ValueError(f'Multiple script subfolders found named \"{args.name}\": {matching_dirs}')
    script_file_path = os.path.join(matching_dirs[0], SCRIPT_FILE_NAME)
    version_file_path = os.path.join(matching_dirs[0], VERSION_FILE_NAME)
    version = read_version_file(version_file_path)
    version_with_name = generate_version_tag(args.name, version)
    repo = git.Repo(search_parent_directories=True)
    commit_hash = get_git_commit_hash(repo, length=40)
    is_release = is_commit_a_release(repo, version_with_name, commit_hash)
    if is_release:
        version_to_use = version_with_name
    else:
        version_to_use = add_commit_to_version_name(version_with_name, commit_hash)
    print(version_to_use)
    # TODO: check if we are a release (version == tag.name && commit == tag.commit)
    # TODO: generate temporary .version file (using git-hash)
    # TODO: build PyInstaller executable
