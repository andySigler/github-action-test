import argparse
import os
import platform
import shutil

import git
from PyInstaller.__main__ import run as build_exe

from .version import read_version_file, get_git_commit_hash
from .version import VERSION_FILE_NAME, DEFAULT_HASH_LENGTH


RELATIVE_SCRIPTS_DIR = '../scripts'
TEMP_PY_NAME = 'tmp.py'  # the actual script PyInstaller builds


def generate_version_tag(name, version):
    return name + '_' + version


def add_commit_to_version_name(name, hash):
    return name + '_' + hash[:DEFAULT_HASH_LENGTH]


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


def fix_path_for_windows(path):
    if platform.system() == 'Windows':
        return path.replace('\\', '\\\\')
    return path


def convert_dir_to_py_import(exclude, path):
    module_path = [os.path.basename(path)]
    while len(module_path) < 10:
        path = os.path.split(path)[0]
        dir_name = os.path.basename(path)
        if dir_name == exclude:
            module_path.reverse()
            return '.'.join(module_path)
        module_path.append(os.path.basename(path))
    raise ValueError(
        f'Unable to find parent directory ({exclude}) within script path ({path})')

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Script Build")
    parser.add_argument(
        "-n",
        "--name",
        help="Subfolder name containing the target script to build (__main__.py)",
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
    args = parser.parse_args()

    # find the directory containing our target script (args.name)
    scripts_dir = os.path.join(os.path.dirname(__file__), RELATIVE_SCRIPTS_DIR)
    matching_dirs = search_for_subfolder_by_name(scripts_dir, args.name)
    if not len(matching_dirs):
        raise ValueError(f'No script subfolders found named \"{args.name}\"')
    if len(matching_dirs) > 1:
        # TODO: maybe make a list to pick which one to build?
        raise ValueError(f'Multiple script subfolders found named \"{args.name}\": {matching_dirs}')
    version_file_path = os.path.join(matching_dirs[0], VERSION_FILE_NAME)

    # read .version file, create a name_version string
    version = read_version_file(version_file_path)
    version_with_name = generate_version_tag(args.name, version)

    # check if this current commit is a release or not (is a release if it was tagged)
    repo = git.Repo(search_parent_directories=True)
    commit_hash = get_git_commit_hash(repo, length=40)
    is_release = is_commit_a_release(repo, version_with_name, commit_hash)
    if is_release:
        version_to_use = str(version_with_name)
    else:
        # if NOT a release, then append the commit hash to the version string
        version_to_use = add_commit_to_version_name(version_with_name, commit_hash)

    # generate temporary .version and main.py files
    build_dir = os.path.abspath('./build')
    tmp_version_file_path = os.path.join(build_dir, VERSION_FILE_NAME)
    tmp_py_file_path = os.path.join(build_dir, TEMP_PY_NAME)
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.mkdir(build_dir)
    with open(tmp_version_file_path, 'w') as f:
        f.write(version_to_use)
    repo_name = repo.remotes.origin.url.split('.git')[0].split('/')[-1]
    import_py_line = convert_dir_to_py_import(repo_name, matching_dirs[0])
    with open(tmp_py_file_path, 'w') as f:
        f.write(f'from {import_py_line} import main; main()')
    embedded_data_path = fix_path_for_windows(tmp_version_file_path)
    if platform.system() == 'Windows':
        embedded_data_path += ';.'
    else:
        embedded_data_path += ':.'

    # build PyInstaller executable, using temporary files
    pyinstaller_args = [
        fix_path_for_windows(tmp_py_file_path), '--clean', '--onefile',
        '--name', version_to_use, '--distpath', fix_path_for_windows(build_dir), '-y',
        '--add-data', embedded_data_path
    ]
    with open(os.path.join(build_dir, 'pyinstaller.sh'), 'w') as f:
        f.write('pyinstaller ' + ' '.join(pyinstaller_args))
    build_exe(pyinstaller_args)
