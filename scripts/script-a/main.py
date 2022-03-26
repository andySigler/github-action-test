import configparser
import os
from pathlib import PurePath
import sys

import git


VERSION_FILE_NAME = '.version'
CONFIG_FILE_NAME = 'config.ini'


def is_frozen():
    is_pyinstaller = getattr(sys, 'frozen', False)
    is_py_file = (not is_pyinstaller) and __file__
    if not is_pyinstaller and not is_py_file:
        raise RuntimeError('Unexpected state: not frozen nor __file__')
    return is_pyinstaller


def get_git_commit_hash(length=7):
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.commit.hexsha
    return repo.git.rev_parse(sha, short=length)


if __name__ == '__main__':
    print('\n------- ENTER -------\n')

    if is_frozen():
        # TODO: this shouldn't be the actual folder of the executable
        #       but should instead be the executables internal folder
        THIS_DIR = PurePath(sys._MEIPASS)
        config_filepath = os.path.join(sys._MEIPASS, CONFIG_FILE_NAME)
        config = configparser.ConfigParser()
        config.read(config_filepath)
        print(config)
        print(config['DEFAULT'])
        print(config['DEFAULT']['Version'])
    else:
        version_filepath = os.path.join(PurePath(os.path.dirname(__file__)), VERSION_FILE_NAME)
        with open(version_filepath, 'r') as f:
            latest_tagged_version = f.readlines()[0].strip()
        version = f'{latest_tagged_version}-PY-{get_git_commit_hash()}'
        print(version)


    print('\n------- EXIT -------\n')
