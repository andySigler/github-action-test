import sys
import os


def get_version():
    '''
        Three states the software can be in:
            - Python script
            - Compiled executable
            - Compiled executable for release

        Three version formats for each state:
            - <version>-<hash>-DEV
            - <version>-<hash>
            - <version>

        Differentiate executable for release using environment variable
            - IS_RELEASE

        
    '''
    VERSION = None
    is_pyinstaller = getattr(sys, 'frozen', False)
    if is_pyinstaller:
        THIS_DIR = PurePath(os.path.dirname(sys.executable))
    elif __file__:
        THIS_DIR = PurePath(os.path.dirname(__file__))
        # TODO: get the git commit, and append
    else:
        raise RuntimeError('Unexpected state: not frozen nor __file__')
