import time

# because this is a Python package, we can do relative imports
# NOTE: we can NO LONGER "insert" paths to scripts
#       this would prevent us from being able to "freeze" into an EXE
from ...utils.version import generate_script_version
from ...drivers.example_driver import example_driver_method
from .helper import helper_method


# all test scripts require a main() method
# this replaces the (__name__ == '__main__') section
def main():
    # script version must be stored in the ".version" file next to __init__.py
    print('Script version:', generate_script_version(__file__))
    while True:
        time.sleep(1)
        print(helper_method())
        print(example_driver_method())
