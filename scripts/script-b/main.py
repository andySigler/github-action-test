import sys
import os


VERSION = None
if getattr(sys, 'frozen', False):
    # running as PyInstaller executable
    THIS_DIR = PurePath(os.path.dirname(sys.executable))
elif __file__:
    # running as Python script
    THIS_DIR = PurePath(os.path.dirname(__file__))
    # TODO: get the git commit, and append
else:
    raise RuntimeError('Unexpected state: not frozen nor __file__')