import argparse
import os
import platform
import shutil

import git
from PyInstaller.__main__ import run as build_exe

from .version import read_version_file, get_git_commit_hash, add_commit_hash_to_version
from .version import VERSION_FILE_NAME


RELATIVE_BUILD_DIR = './build'
RELATIVE_SCRIPTS_DIR = '../production_tests'
TEMP_PY_NAME = 'tmp.py'  # the actual script PyInstaller builds
MAIN_PY_NAME = 'main.py'


def generate_version_tag(name, version):
    return name + '-' + version


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


def fix_path_for_pyinstaller(path):
    if platform.system() == 'Windows':
        path = path.replace('\\', '\\\\')
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


def find_version_file_path(name):
    scripts_dir = os.path.join(os.path.dirname(__file__), RELATIVE_SCRIPTS_DIR)
    matching_dirs = search_for_subfolder_by_name(scripts_dir, name)
    if not len(matching_dirs):
        raise ValueError(f'No script subfolders found named \"{args.name}\"')
    if len(matching_dirs) > 1:
        # TODO: maybe make a list to pick which one to build?
        raise ValueError(f'Multiple script subfolders found named \"{args.name}\": {matching_dirs}')
    return os.path.join(matching_dirs[0], VERSION_FILE_NAME)


def generate_tag_name_for_script(name):
    # this method is used while tagging releases (GithubAction)
    return generate_version_tag(name, read_version_file(find_version_file_path(name)))



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
        default=RELATIVE_BUILD_DIR,
        type=str,
    )
    args = parser.parse_args()

    # read .version file
    version_file_path = find_version_file_path(args.name)
    version = read_version_file(version_file_path)

    # get the main script path
    main_file_path = os.path.join(os.path.dirname(version_file_path), MAIN_PY_NAME)

    # check if this current commit is a release or not (is a release if it was tagged)
    repo = git.Repo(search_parent_directories=True)
    expected_tag_name = generate_version_tag(args.name, version)
    is_release = is_commit_a_release(
        repo, expected_tag_name, get_git_commit_hash(repo, length=40))
    if not is_release:
        version = add_commit_hash_to_version(version)

    # generate temporary .version
    build_dir = os.path.abspath(args.out_dir)
    tmp_version_file_path = os.path.join(build_dir, VERSION_FILE_NAME)
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.mkdir(build_dir)
    with open(tmp_version_file_path, 'w') as f:
        f.write(version)
    embedded_data_path = fix_path_for_pyinstaller(tmp_version_file_path)
    if platform.system() == 'Windows':
        embedded_data_path += ';.'
    else:
        embedded_data_path += ':.'

    # build PyInstaller executable, using temporary files
    build_name = generate_version_tag(args.name, version)
    pyinstaller_args = [
        fix_path_for_pyinstaller(main_file_path),
        '--clean', '--onefile', '-y',
        '--name', build_name.replace('.', '-'),
        '--add-data', embedded_data_path
    ]
    with open(os.path.join(build_dir, f'build_{build_name}.sh'), 'w') as f:
        f.write('pyinstaller ' + ' '.join(pyinstaller_args))
    build_exe(pyinstaller_args)
    # move the spec file to the ./build dir
    for f in os.listdir('.'):
        if os.path.isfile(f) and f.split('.')[-1] == 'spec':
            os.rename(f, os.path.join(build_dir, f))
    print(f'\nDone building {build_name}')
