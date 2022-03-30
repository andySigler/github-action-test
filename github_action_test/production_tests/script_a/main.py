import time

# NOTE: compiled scripts can NOT insert paths for imports
#       this would prevent us from being able to "freeze" into an EXE

from github_action_test.utils.version import generate_script_version as test_version
from github_action_test.drivers.example_driver import example_driver_method

from github_action_test.production_tests.script_a.helper import helper_method


if __name__ == '__main__':
    # version is stored in ".version" file (next to main.py)
    print('Test version:', test_version(__file__))
    while True:
        print(helper_method())
        print(example_driver_method())
        time.sleep(1)
