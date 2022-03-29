import time

# NOTE: we can NO LONGER "insert" paths to scripts
#       this would prevent us from being able to "freeze" into an EXE
from github_action_test.utils.version import generate_script_version
from github_action_test.drivers.example_driver import example_driver_method

from github_action_test.production_tests.script_a.helper import helper_method


if __name__ == '__main__':
    # script version must be stored in the ".version" file next to __init__.py
    print('Script version:', generate_script_version(__file__))
    while True:
        time.sleep(1)
        print(helper_method())
        print(example_driver_method())
