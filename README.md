# github-action-test

## Installation

### 1) Clone repository:
```commandline
git clone https://github.com/andySigler/github-action-test.git
cd github-action-test
```

### 2) **Optional**: Create a virtual Python environment:

on macOS:
```commandline
python -m virtualenv venv
source venv/bin/activate
```

on Windows:
```commandline
python -m virtualenv venv
./venv/Scripts/activate.bat
```

### 3) Install Python requirements:
```commandline
cd python-code
python setup.py develop
cd ..
```

## Developing

`python_code` is a Python module, and can be invoked from command line using the following syntax:

```commandline
python -m python_code.scripts.script_a
```

This works because the submodule `script_a` is organized like this:

```
github-action-test
    -> python_code
        -> scripts
            -> script_a
                -> __init__.py
                -> __main__.py
                -> .version
```

### __init__.py

This is the entry point for the `script_a` submodule, and must define a `main()` method:

```python
# __init___.py

def main():
    # code goes here
```

### __main__.py

This is the actual file that is called when running as submodule, using `python -m ...`

Every `__main__.py` file can simply contain the following few lines:
```python
# __main__.py
from . import main

if __name__ == '__main__':
    main()
```

This imports the `main()` method from `__init__.py`, and runs it.

### .version

This is a text file containing the current tagged version of this script.

For example, a script my have the version `A1.3`, which would be put inside the `.version` file like this:

```
A1.3
```

This file is read and used to create a unique version string for the script (and built executable).
