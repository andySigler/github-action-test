import time

# because this is a Python package, we can do relative imports
from ...utils.version import generate_script_version
from ...drivers.example_driver import example_driver_method

# however, you can still specifically add some external path
# NOTE: use insert_path() along with __file__ to guarantee it works
from ...utils.insert_path import insert_path
insert_path(__file__, '../../../extra_python')
import some_script


# all test scripts require a main() method
# this replaces the (__name__ == '__main__') section
def main():
    # script version must be stored in the ".version" file next to __init__.py
    print('Script version:', generate_script_version(__file__))
    while True:
        time.sleep(1)
        print(example_driver_method())
        print(some_script.some_outside_method())
