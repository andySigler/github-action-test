import argparse
import os
import platform
import shutil

import git
from PyInstaller.__main__ import run as build_exe

from .version import read_version_file, get_git_commit_hash, add_commit_hash_to_version
from .version import VERSION_FILE_NAME


DIST_DIR = 'dist'
TARGET_DIR_RELATIVE_TO_THIS_FILE = '../production_tests'
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
    scripts_dir = os.path.join(os.path.dirname(__file__), TARGET_DIR_RELATIVE_TO_THIS_FILE)
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
        default=DIST_DIR,
        type=str,
    )
    args = parser.parse_args()

    # read .version file
    version_file_path = find_version_file_path(args.name)
    version = read_version_file(version_file_path)

    # get the main script path
    main_file_path = os.path.join(os.path.dirname(version_file_path), MAIN_PY_NAME)
    if not os.path.exists(main_file_path):
        py_name = f'{args.name}.py'
        main_file_path = os.path.join(os.path.dirname(version_file_path), py_name)
        if not os.path.exists(main_file_path):
            raise FileNotFoundError(
                'Unable to find a script to build (neither \"{MAIN_PY_NAME}\" nor \"{py_name}\")')

    # check if this current commit is a release or not
    # is a release if this commit was tagged
    repo = git.Repo(search_parent_directories=True)
    expected_tag_name = generate_version_tag(args.name, version)
    is_release = is_commit_a_release(
        repo, expected_tag_name, get_git_commit_hash(repo, length=40))
    if not is_release:
        # non-releases get the commit hash added to their version
        version = add_commit_hash_to_version(version)

    # generate .version file to embed in executable
    # put it in a dist folder
    dist_dir = os.path.abspath(args.out_dir)
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.mkdir(dist_dir)
    tmp_version_file_path = os.path.join(dist_dir, VERSION_FILE_NAME)
    with open(tmp_version_file_path, 'w') as f:
        f.write(version)

    # build PyInstaller executable, using temporary files
    build_name = generate_version_tag(args.name, version)
    embedded_data_path = fix_path_for_pyinstaller(tmp_version_file_path)
    if platform.system() == 'Windows':
        embedded_data_path += ';.'
    else:
        embedded_data_path += ':.'
    pyinstaller_args = [
        fix_path_for_pyinstaller(main_file_path),
        '--clean', '--onefile', '-y',
        '--name', build_name.replace('.', '-'),
        '--add-data', embedded_data_path
    ]
    # save the generated pyinstaller command, to help with debugging
    with open(os.path.join(dist_dir, f'build_{build_name}.sh'), 'w') as f:
        f.write('pyinstaller ' + ' '.join(pyinstaller_args))
    build_exe(pyinstaller_args)
    # move the spec file to the ./build dir
    for f in os.listdir('.'):
        if os.path.isfile(f) and f.split('.')[-1] == 'spec':
            os.rename(f, os.path.join(dist_dir, f))

    print(f'\nDone building {build_name}')
