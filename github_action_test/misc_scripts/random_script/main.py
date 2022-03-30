import os
import sys
import time

# you can still insert paths for imports, but you cannot compile these scripts
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'../../drivers'))
from example_driver import example_driver_method

# you can still use package import syntax, at the same time as inserting to the path
from github_action_test.misc_scripts.random_script.helper import helper_method


if __name__ == '__main__':
    while True:
        print(helper_method())
        print(example_driver_method())
        time.sleep(1)
