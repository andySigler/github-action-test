# github-action-test

## Installing

1) Clone the repo
2) `cd` into repo directory
3) Install the `github_action_test` Python package, in editable (`-e`) mode

```commandline
git clone https://github.com/andySigler/github-action-test.git
cd github-action-test
python -m pip install -e .
```

## Developing

`github_action_test` is a Python module, and can be invoked from command line using the following syntax:

```commandline
python -m github_action_test.scripts.script_a
```

This works because the submodule `script_a` is organized like this:

```
github-action-test
    -> github_action_test
        -> production_tests
            -> script_a
                -> .version
                -> main.py
                -> whatever_script_you_want.py
```

### .version

This is a text file containing the current tagged version of this script.

For example, a script my have the version `A1.3`, which would be put inside the `.version` file like this:

```
A1.3
```

This file is read and used to create a unique version string for the script (and built executable).

### main.py

This is the entry point for the `script_a` submodule. It is required to be named `main.py`, for use during PyInstaller builds:

```python
# main.py

if __name__ == '__main__':
    # code goes here
```

## Release

### Versioning

Updates made to a script's version are done by editing its contained `.version` file.

When creating a new version, and pull-request should be made which contains only the update to the `.version` file. This makes it easier to have simultaneous pull-requests while preparing a version update.

### Building

Executables are generated for macOS and Windows, using a GithubAction workflow.

The `build_release` GithubAction workflow can be initiated at any time, to create a release:
1) Run workflow with input
   1) script name
2) Workflow sets up environment
3) Downloads repo
4) Generates a tag, and pushes to Github
   1) Generate tag name using Python (generate_tag_name_for_script())
   2) Compare with other tags to guarantee uniqueness
5) Builds script
6) Uploads EXE or ZIP

### Releasing

Download the EXE and ZIP artifacts generated by the workflow.

Navigate on Github to the newly generated tag. Click the `Edit` button.

Enter all applicable information.

Attach the EXE and ZIP files to this release, and publish.
