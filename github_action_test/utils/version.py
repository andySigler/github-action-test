import os
import sys

import git


VERSION_FILE_NAME = '.version'
DEFAULT_HASH_LENGTH = 7


def is_frozen() -> bool:
    _frozen = getattr(sys, 'frozen', False)
    if not _frozen and not __file__:
        raise RuntimeError('Unexpected state: not frozen nor __file__')
    return _frozen


def get_git_commit_hash(repo=None, length=DEFAULT_HASH_LENGTH):
    if not repo:
        repo = git.Repo(search_parent_directories=True)
    _sha = repo.head.commit.hexsha
    return repo.git.rev_parse(_sha, short=length)


def add_commit_hash_to_version(version, repo=None, length=DEFAULT_HASH_LENGTH):
    return f'{version}-{get_git_commit_hash(repo=repo, length=length)}'


def read_version_file(version_filepath) -> str:
    if not os.path.exists(version_filepath):
        raise RuntimeError(
            f'Unable to find version file at path: \"{version_filepath}\"')
    with open(version_filepath, 'r') as f:
        lines = f.readlines()
        if not len(lines):
            raise RuntimeError(
                f'No version found in \"{version_filepath}\"')
        version = lines[0].strip()
    if not version:
        raise RuntimeError(
            f'No version found in \"{version_filepath}\"')
    return version


def generate_script_version(file) -> str:
    is_pyinstaller = is_frozen()
    if is_pyinstaller:
        version_dir = sys._MEIPASS
    else:
        # version file is stored next to the Python script being invoked
        version_dir = os.path.dirname(file)
    version_filepath = os.path.join(version_dir, VERSION_FILE_NAME)
    version = read_version_file(version_filepath=version_filepath)
    if not is_pyinstaller:
        # Python script automatically appends the commit hash to version
        version = add_commit_hash_to_version(version)
    return version
