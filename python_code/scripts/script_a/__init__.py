import time

from ...utils.script_version import generate_script_version
from ...drivers.example_driver import example_driver_method


def main():
    while True:
        time.sleep(1)
        print(generate_script_version())
        print(example_driver_method())
